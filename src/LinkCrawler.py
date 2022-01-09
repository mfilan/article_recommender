import re

from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Crawler(CrawlSpider):
    name = "crawler"
    rules = (Rule(LinkExtractor(allow=('^https?://en.wikipedia.org/wiki.*',)), follow=True, callback='parse_item'),)

    start_urls = [
        "https://en.wikipedia.org/wiki/Information_retrieval",
    ]
    custom_settings = {
        'FEEDS': {
            '../data/links.txt': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse_item(self, response):
        if len(re.findall(":", response.url)) >= 2:
            pass
        else:

            yield {
                'link': response.url
            }


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Crawler)
    process.start()