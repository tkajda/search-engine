import requests as req
from urllib.parse import urljoin
import bs4
import logging

logging.basicConfig(
    format = '%(asctime)s %(levelname)s:%(message)s',
    level = logging.INFO)


class Crawler:

    def __init__(self, urls=[], file_counter=0, num_of_files=int(5e4)):
        self.visited_urls = {}
        self.urls_to_visit = urls
        self.file_counter = file_counter
        self.start_of_url = 'https://en.wikipedia.org'
        self.num_of_files = num_of_files

    def download_url(self, url):
        return req.get(url).text

    def write_text_to_file(self, article, f_name):
        if article:
            self.file_counter += 1
            path = 'articles/' + str(f_name[6:]) + '.txt'
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(article.text)

    def get_linked_a(self, html, f_name):
        a = {}
        soup = bs4.BeautifulSoup(html, 'html.parser')
        article = soup.find('div', {"class": "mw-parser-output"})
        self.write_text_to_file(article, f_name)

        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/wiki') and path[6:11] != 'File:':
                a[path] = path

        return a

    def crawl(self, url, f_name):
        html = self.download_url(url)
        for single_a_tag in self.get_linked_a(html, f_name).values():
            if single_a_tag and len(self.urls_to_visit) < 130 and single_a_tag not in self.urls_to_visit and single_a_tag not in self.visited_urls:
                self.urls_to_visit.append(single_a_tag)

    def run(self):

        while self.urls_to_visit and self.file_counter < self.num_of_files:
            tmp = self.urls_to_visit.pop(0)
            url = str(self.start_of_url) + str(tmp)
            try:
                logging.info(f'Crawling: {url}')
                self.visited_urls[tmp] = 1
                self.crawl(url, tmp)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')


