from flask import Flask
from flask import request
import logging

from logic.Parser import Parser
from logic.SearchEngine import SearchEngine
from logic.WebCrawler import Crawler


class Server:
    def __init__(self, number_of_results=10, svd_k=100, prepare_necc_files=False):
        self.se = SearchEngine(number_of_results=number_of_results,
                               svd_k=svd_k,
                               search_svd=True,
                               prepare_necc_files=prepare_necc_files)
        self.app = Flask(__name__)

        @self.app.route("/search", methods=['POST'])
        def find_results():
            req = str(request.data.decode())
            req = req[1:]
            req = req[:-1]
            logging.log(req)
            try:
                response_data = self.se.search(req)
            except IOError:
                return {"links": "Could not find articles"}

            return {"links": response_data}

    def run(self):
        self.app.run()


if __name__ == "__main__":
    # Crawler(['/wiki/Tea']).run()
    # Parser().run()
    engine = Server(number_of_results=15, prepare_necc_files=True)
    engine.run()
    del engine
