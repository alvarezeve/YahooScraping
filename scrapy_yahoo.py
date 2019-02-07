import scrapy
import time


class YahooSpider(scrapy.Spider):
	name = "Yahoo"
	allowed_domains = ["finance.yahoo.com"]
	start_urls = ['https://finance.yahoo.com/quote/VTV?p=VTV']
	def parse(self, response):
		print("hola")
		print(response.css("script"))
		crumb = response.css('script').re_first('user":{"crumb":"(.*?)"').decode('unicode_escape')
		print(crumb)
		#url = ("https://query1.finance.yahoo.com/v7/finance/download/FB" +
		#       "?period1=-2208988800&period2=" + str(int(time.time())) + "&interval=1d&events=history&" +
		#       "crumb={}".format(crumb))
		return scrapy.Request(callback=self.parse_csv)

	def parse_csv(self, response):
		lines = response.body.strip().split('\n')
		#print(lines[0])
		#print(lines[1])
		#print(lines[-1])
