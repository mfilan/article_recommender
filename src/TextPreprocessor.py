import os
import re
from multiprocessing import Pool

import requests
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


class TextPreprocessor:
    def __init__(self, headers=None):
        self.preprocessed_data_path = os.path.join('../data', 'processed_data')
        self.nlp = spacy.load("en_core_web_sm")
        self.stemmer = SnowballStemmer(language='english')
        self._stop_words = set(stopwords.words('english'))
        self.headers = headers
        super(TextPreprocessor, self).__init__()

    @staticmethod
    def read_links(path):
        with open(path, "r", encoding='utf-8') as fp:
            links = fp.read().replace('"', "").split("\n")[1:]
        return links

    @staticmethod
    def filter_chars(text):
        text = re.sub("\ufeff", " ", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        text = " ".join([i for i in text.split() if len(i) > 1])
        return text.lower()

    def preprocess_text(self, text):
        doc = self.nlp(self.filter_chars(text))
        doc = [self.stemmer.stem(token.lemma_) for token in doc if token.lemma_.lower() not in self._stop_words]
        return " ".join(doc)

    def preprocess_data(self, url):
        response = requests.request("GET", url, headers=self.headers, data={})
        soup = BeautifulSoup(response.text, features="lxml")
        preprocessed_text = self.preprocess_text(" ".join([i.text for i in soup.find_all("p")]))
        return [preprocessed_text]

    def create_preprocessed_data(self, url):
        response = requests.request("GET", url, headers=self.headers, data={})
        soup = BeautifulSoup(response.text, features="lxml")
        preprocessed_text = self.preprocess_text(" ".join([i.text for i in soup.find_all("p")]))
        with open(os.path.join(self.preprocessed_data_path, url.split("/")[-1] + ".txt"), 'w') as fp:
            fp.write(preprocessed_text)


if __name__ == "__main__":

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'WMF-Last-Access=08-Jan-2022; WMF-Last-Access-Global=08-Jan-2022; '
                  'enwikiwmE-sessionTickLastTickTime=1641645721920; enwikiwmE-sessionTickTickCount=20; '
                  'GeoIP=PL:30:Poznan:52.41:16.93:v4; enwikimwuser-sessionId=1b0b231cd1f7acb09f89; '
                  'enwikiel-sessionId=3039b7160aca334a2b83',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }
    processor = TextPreprocessor(headers=headers)
    links = processor.read_links("../data/links.txt")
    with Pool() as p:
        print(p.map(processor.create_preprocessed_data, links))