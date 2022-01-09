## Wikipedia articles recommender

### Crawling and scrapping
Data created by crawling through wikipedia pages using CrawlSpider (scrapy) and saving url links to file locates in data/links.txt.
Having obtained links of interest we scrapped given pages using BeautifulSoup in a parallel manner.
### Data preprocessing 
As the key idea is to recommend similar pages based on the content of the articles we decided to filter all non-words strings e.g. commas, dots, dates or coordinates.
Furthermore, we removed english stopwords from the articles as they are irrelevant. Resulting words were lemmatized (using spacy) and stemmed (using nltk). Obtained data was saved in the data/processed_data folder.
### Recommending articles
Cached, preprocessed articles were read to obtain tf-idf (term frequency - inverse document frequency) matrix. Inference can be divided in the following steps:
* scrapping the pages of interest 
* preprocessing read articles
* transforming obtained data into learned vector space
* calculating cosine similarity between each page of interest and our database
* returning N most similar pages for each passed page

### Statistics  & interpretation
Our database consists of 5676 articles. For further statistics and interpretation please take a look at analyzes.ipynb
### Usage 
Create venv and install libraries
```
python3 -m venv recommender 
source recommender/bin/activate
pip3 install -r requirements.txt
```
Inference 
```
from ArticleRecommender import ArticleRecommender
recommender = ArticleRecommender()
recommender.load()
recommend_articles = recommender.recommend_articles_from_loaded(<list_of_urls>)
```
Project created by: Maciej Filanowicz & Mikołaj Kruś


