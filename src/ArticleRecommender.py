import logging
import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from TextPreprocessor import TextPreprocessor

logging.getLogger().setLevel(logging.INFO)


class ArticleRecommender(TextPreprocessor, TfidfVectorizer):
    def __init__(self, **kwargs):
        super(ArticleRecommender, self).__init__(**kwargs)
        self.tfidf = None
        self.files = None

    def prepare_new_url(self, url):
        return self.transform(self.preprocess_data(url))

    def get_similarities(self, url, tfidf):
        return linear_kernel(self.prepare_new_url(url), tfidf).flatten()

    def recommend_articles(self, url, tfidf, files, n_articles=5):
        cosine_sim = self.get_similarities(url, tfidf)
        related_docs_indices = cosine_sim.argsort()[:-n_articles:-1]
        return list(zip(np.array(files)[related_docs_indices],
                        cosine_sim[related_docs_indices]))

    def load(self, preprocessed_data_path=os.path.join('../data', 'processed_data')):

        self.files = [os.path.join(preprocessed_data_path, file)
                      for file in os.listdir(preprocessed_data_path)]
        logging.info(f"Reading {len(self.files)} articles...")
        data = [open(file, 'r', encoding='utf-8').read() for file in self.files]
        logging.info(f"Learning vocabulary and inverse document frequency...")
        self.fit(data)
        logging.info(f"Vectorizing articles...")
        self.tfidf = self.transform(data)

    def recommend_articles_from_loaded(self, urls, n_articles=5):
        recommended_articles = {}
        for url in urls:
            cosine_sim = self.get_similarities(url, self.tfidf)
            related_docs_indices = cosine_sim.argsort()[:-n_articles:-1]
            related_urls = np.array(self.files)[related_docs_indices]
            related_urls_scores = cosine_sim[related_docs_indices]
            recommended_articles[url] = [{"recommended_url": "http://en.wikipedia.org/wiki/" + link.split("/")[-1].rstrip(".txt"),
                                          'score': score} for link, score in zip(related_urls, related_urls_scores)]
        return recommended_articles


if __name__ == "__main__":
    recommender = ArticleRecommender()
    recommender.load()
    print(recommender.recommend_articles_from_loaded(["https://en.wikipedia.org/wiki/Polish_language"]))