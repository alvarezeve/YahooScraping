import scrapy
from scrapy.crawler import CrawlerProcess
class MarilynMansonQuotes(scrapy.Spider):
    name = "MarilynMansonQuotes"
    start_urls = [
        'https://en.wikiquote.org/wiki/Marilyn_Manson',
    ]

    def parse(self, response):
        for quote in response.css('div.mw-parser-output > ul > li'):
            yield {'quote': quote.extract()}
process = CrawlerProcess()
process.crawl(MarilynMansonQuotes)
process.start()
