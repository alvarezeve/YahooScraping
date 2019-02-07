#....................................Extract data from Yahoo Finance....................................
#_______________________________________This is a test ________________________________

#Import library
from lxml import html
import requests
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy import update

# for analizer the url using a parse method, works one by one (VTV,VOE,...)
def parse(ticker):
	url = "http://finance.yahoo.com/quote/%s?p=%s&.tsrc=fin-srch"%(ticker,ticker) #pass the url
	response = requests.get(url, verify=False) # get the information from object request
	print ("Parsing %s"%(url)) #show a url for analizer, only format
	sleep(4) #make a pause only for get a time in the explorer
	parser = html.fromstring(response.text) #from object response using atribute text
	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr') #give the Xpath to the content
	summary_data = OrderedDict() #for remember the order in dictionary and create a summary
	other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
	summary_json_response = requests.get(other_details_json_link) #get more info
	try:
		json_loaded_summary =  json.loads(summary_json_response.text) #try to extract text from sumary
		eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"] #exctract statistics info
		datelist = []
		for table_data in summary_table:
			raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()') #for read infor from begin
			raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()') #at the end
			table_key = ''.join(raw_table_key).strip()
			table_value = ''.join(raw_table_value).strip()
			summary_data.update({table_key:table_value}) #join or link the data
		return summary_data
	except:
		print ("Failed to parse json response")
		return {"error":"Failed to parse json response"}



#now we do everything
if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('ticker',help = '') #for read and help the user
	args = argparser.parse_args()
	ticker = args.ticker #value of active
	print ("Fetching data for %s"%(ticker)) #only format
	scraped_data = parse(ticker) #using the parse method
	print ("Writing data to output file") #Ready!
	with open('%s-summary.json'%(ticker),'w') as fp:
		json.dump(scraped_data,fp,indent = 4)
#for actualize the table called FinanceY. The actives are rows in FinanceY and the financel data are columns
PC = scraped_data.items()[0][1] #asign a var for each data
OP = scraped_data.items()[1][1]
DR = scraped_data.items()[4][1]
WR52 = scraped_data.items()[5][1]
V = scraped_data.items()[6][1]
NAV_V = scraped_data.items()[9][1]
PER = scraped_data.items()[10][1]
Y = scraped_data.items()[11][1]
D = scraped_data.items()[15][1]

db_string = "postgresql://postgres:evelyn@localhost:5432/postgres" #path for my data base

db = create_engine(db_string) #object called db because is data base
#one by one only because is to large and unconfortable in one line
db.execute("UPDATE FinanceY SET PreviousClose=%s WHERE Activo=%s",(PC,ticker)) #update the database
db.execute("UPDATE FinanceY SET OpenPrice=%s WHERE Activo=%s",(OP,ticker))
db.execute("UPDATE FinanceY SET DaysRange=%s WHERE Activo=%s",(DR,ticker))
db.execute("UPDATE FinanceY SET WeekRange52=%s WHERE Activo=%s",(PC,ticker))
db.execute("UPDATE FinanceY SET Volume=%s WHERE Activo=%s",(V,ticker))
db.execute("UPDATE FinanceY SET NAV=%s WHERE Activo=%s",(NAV_V,ticker))
db.execute("UPDATE FinanceY SET PE_Ratio=%s WHERE Activo=%s",(PER,ticker))
db.execute("UPDATE FinanceY SET FechaConsulta=%s WHERE Activo=%s",(D,ticker))
db.execute("UPDATE FinanceY SET Yield=%s WHERE Activo=%s",(Y,ticker))

# Read
result_set = db.execute("SELECT * FROM FinanceY")
for r in result_set:
    print(r)
#end
