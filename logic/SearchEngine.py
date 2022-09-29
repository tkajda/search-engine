from os.path import exists
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import scipy.sparse
from sklearn.decomposition import TruncatedSVD
import pickle
import numpy as np
from sklearn.preprocessing import normalize
import logging


class SearchEngine:

    def __init__(self, number_of_results, svd_k, search_svd, prepare_necc_files):
        self.directory = 'parsed-files'
        self.all_files = glob.glob(f"{self.directory}/*")
        self.stemmer = PorterStemmer()
        self.num_of_results = number_of_results

        if prepare_necc_files:
            self.prepare_files(svd_k)

        self.tfidf_matrix = scipy.sparse.load_npz("matrixes/tfidf_matrix.npz").T
        self.vocab = self.load_vocab()
        if search_svd:
            if svd_k == 100:
                self.svd_matrix = np.load("matrixes/svd_matrix.npz")['svd_matrix']
                self.svd_components = np.load("matrixes/svd_comps.npz")['svd_comps']
            else:
                svd = TruncatedSVD(n_components=svd_k).fit(self.tfidf_matrix.T)
                self.svd_matrix = svd.transform(self.tfidf_matrix.T)
                self.svd_components = svd.components_

            self.search_function = self.search_with_svd
        else:
            self.search_function = self.search_with_no_svd

    def load_vocab(self):
        a_file = open("matrixes/union.pkl", "rb")
        vocab = pickle.load(a_file)
        a_file.close()
        return vocab

    def handle_input(self, inp):
        stemmed_words = [self.stemmer.stem(word) for word in inp.split()]
        input_vector = np.zeros(shape=self.tfidf_matrix.shape[0])
        for word in stemmed_words:
            if self.vocab.__contains__(word):
                input_vector[self.vocab[word]] += 1
        if len(input_vector) == 0:
            raise IOError

        return self.search_function(input_vector)

    def search(self, input):
        return self.handle_input(input)

    def parse_result(self, res):
        def parse_title(title):
            for i in range(len(title)):
                if title[i] == "@":
                    newstr = str(title[i + 1:])
                    return str(newstr[:-4])

        result_json = []
        for i in range(self.num_of_results):
            result_json.append(
                {"link": "https://en.wikipedia.org/" + parse_title(str(self.all_files[res[i][0]]))}
            )

        return result_json

    def prepare_files(self, svd_k):
        all_files = self.all_files if self.all_files else glob.glob(f"{self.directory}/*")

        if not exists("matrixes/tfidf_matrix.npz") \
                or not exists("matrixes/svd_matrix.npz") \
                or not exists("matrixes/union.pkl") \
                or not exists("matrixes/svd_comps.npz"):

            tfidf_vec = TfidfVectorizer(input='filename')
            matrix = tfidf_vec.fit_transform(all_files)
            svd = TruncatedSVD(n_components=svd_k).fit(matrix)
            svd_matrix = svd.transform(matrix)
            svd_components = svd.components_

            if not exists("matrixes/tfidf_matrix.npz"):
                scipy.sparse.save_npz("matrixes/tfidf_matrix", matrix, compressed=True)

            if not exists("matrixes/union.pkl"):
                a_file = open("matrixes/union.pkl", "wb")
                pickle.dump(tfidf_vec.vocabulary_, a_file)
                a_file.close()

            if not exists("matrixes/svd_matrix.npz"):
                np.savez_compressed("matrixes/svd_matrix", svd_matrix=svd_matrix)

            if not exists("matrixes/svd_comps.npz"):
                np.savez_compressed("matrixes/svd_comps", svd_comps=svd_components)

    def search_with_svd(self, input_vector):
        svd_inp = self.svd_components @ input_vector
        svd_q = self.svd_matrix @ svd_inp
        res = [(document_id, svd_q[document_id]) for document_id in range(len(self.all_files))]
        res.sort(key=lambda x: x[1], reverse=True)

        logging.log("with svd")
        for i in range(self.num_of_results):
            logging.log(self.all_files[res[i][0]])

        return self.parse_result(res[:self.num_of_results])

    def search_with_no_svd(self, input_vector):

        sparse_vec = normalize(scipy.sparse.csr_matrix(input_vector))
        matrix = normalize(self.tfidf_matrix, axis=0)

        res = sparse_vec @ matrix
        x = []
        for i in range(res.shape[1]):
            tmp = res.getcol(i).data
            if len(tmp) > 0:
                x.append((i, tmp[0]))

        x.sort(key=lambda x: x[1], reverse=True)
        logging.log("without svd")
        for i in range(self.number_of_results):
            print(self.all_files[x[i][0]])

        return self.parse_result(x[:self.num_of_results])
