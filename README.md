# Search Engine
## `Overview`
Wikipedia articles are saved as files and stemmed on the base of their origin for example:
 - **cat**s, **cat**like, **cat**ty = *cat*
 - **arg**ue, **arg**ued, **arg**ues, **arg**uing, **arg**us = *arg* etc.
 
Subsequently, with the use of Singular Value Decomposition [[See more](https://en.wikipedia.org/wiki/Singular_value_decomposition)] algorithm searches in mentioned above files the best results as for vector correlation with entry phrase.

---
## `Model`
### *Crawler*
Crawles at specific site on english wikipedia and downloads the text of article and saves it as a file with specific name.
Crawler also looks for tags which contains links to be visited, so "crawling" is possible. Only wikipedia sites are taken into account.

---
### *Parser*
File parser uses tools of ntlk library to make it possible to stem text in the correct way. Each file is:
 - splitted into separate words
 - filtered so it do not include words which are considered as stop words and shorter than 2 characters
 - stemmed with the use of PorterSteemer
 - new content is saved to a different file
 
 ---
### *SearchEngine*
Class SearchEngine is responsible for numeric site. It allows to look for articles in two ways:
 - without SVD factorization
 - with SVD factorization of degree N (defaults to: 100)
 
The simplest idea behind it is to make a dictionary (union) of words in all files and based on it create matrix that, for each file, assings a vector with the count of each word for a specific text. The top result would be a scalar of the correlation between entry phrase and the vector of the file. Though, obviously longer texts include more words, so it is not necesserly best idea to use this type of matrix. <br>
There comes TF-IDF matrix (TF-IDF is acronym of term-frequency inverse-document-frequency) which is much better to work with as it respects also the length of the text. It is built with the use of TfidfVectorizer of Sklearn package. <nr>
Thanks to this we obtain matrix of shape: (count_of_words_in_union, count_of_files). To avoid high time complexity arrays/queues/matrixes are replaced by dictionaries/sparse-matrixes where is was possible and are loaded from a file if run for a second+ time.

Entering a phrase to search steps are similiar: words are stemmed and vector of the sentence is build based on forementioned union. The result is k highest values of multiplication of entry-phrase-vector and tf-idf-matrix.

---
## `Proof of concept`
As an example I collected 45000+ files of wikipedia articles with the union of words at size > 1 100 000. I have also prepared basic front-end [[here](https://github.com/tkajda/search-engine/tree/main/front-end/search-engine-front-end)] and default Flask server which handles the request [here](https://github.com/tkajda/search-engine/blob/main/main.py)]


<p align="center">
  <img src="https://github.com/tkajda/search-engine/blob/main/images/search-engine-test-1.png" />
</p>
<p align="center">
  <img src="https://github.com/tkajda/search-engine/blob/main/images/search-engine-test-2.png" />
</p>
<p align="center">
  <img src="https://github.com/tkajda/search-engine/blob/main/images/search-engine-test-3.png" />
</p>
Algorithm seems to be working fine ;)
