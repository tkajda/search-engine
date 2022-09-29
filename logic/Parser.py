from os.path import exists
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import codecs
import os


class Parser:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.directory = 'articles'

    def stem_text(self, text):
        """
            Stem text
            Delete stop words in English
            Limit articles to 10k words
            Include word only if has more than 2 letter
            Include word if contains only letters and numbers
        """

        def filter_words(word):
            return not (word in self.stop_words)

        def is_correct(word):
            return len(word) > 2 and word.isalpha()

        tokens = word_tokenize(text)
        word_limit_per_article = int(1e4)
        words_list = []

        for i, word in enumerate(tokens):
            if filter_words(word) and is_correct(word):
                words_list.append(word)
            if i > word_limit_per_article:
                break

        for i, w in enumerate(words_list):
            words_list[i] = self.stemmer.stem(w)
        res = " ".join(words_list)

        return res

    # open file and write parsed text
    def parse_file(self, file_name, new_name):
        res = ""
        with codecs.open(file_name, 'r', errors="ignore", encoding="utf-8") as f:
            for line in f.readlines():
                if not line.isspace():
                    res += line
        res1 = self.stem_text(res)
        with codecs.open(new_name, 'w+', errors="ignore", encoding="utf-8") as f:
            f.write(res1)

    def run(self):
        parsed_files = 'parsed-files/'
        for i, filename in enumerate(os.listdir(self.directory)):
            file_name = os.path.join(self.directory, filename)
            new_name = parsed_files + str(i) + "@" + filename
            if exists(file_name):
                self.parse_file(file_name, new_name)

