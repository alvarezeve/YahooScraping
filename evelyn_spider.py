#....................................Extract data from Yahoo Finance....................................
#_______________________________________This is a test for Theo________________________________

#Import library
from lxml import html
import requests
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep

from sqlalchemy import create_engine
#from sqlalchemy import update
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine, MetaData, Table
#from sqlalchemy.orm import mapper, sessionmaker



#definition of parse (analizer), the method parse analize the url yahoo finance
# for each case of item (VTV,VOE,VTI, etc.)
def parse(ticker):
	#https://finance.yahoo.com/quote/SCHF?p=SCHF&.tsrc=fin-srch
	url = "http://finance.yahoo.com/quote/%s?p=%s&.tsrc=fin-srch"%(ticker,ticker) #pass the url
	response = requests.get(url, verify=False) # get the information from object request
	print ("Parsing %s"%(url)) #show a url for analizer
	sleep(4) #make a pause only for get a time
	parser = html.fromstring(response.text) #from object response using atribute text for extract string
	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr') #give the path
	summary_data = OrderedDict() #for remember the order in dictionary
	other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
	summary_json_response = requests.get(other_details_json_link)
	try:
		#print ("Parsing %s"%(url))
		json_loaded_summary =  json.loads(summary_json_response.text)
		#print (json_loaded_summary["quoteSummary"]["result"][0])
		eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]
		datelist = []
		#print ("Parsing %s"%(url))
		for table_data in summary_table:
			raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
		#	print(raw_table_key)
			raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
			#print(raw_table_value[0])
			table_key = ''.join(raw_table_key).strip()
			table_value = ''.join(raw_table_value).strip()
			summary_data.update({table_key:table_value})
		#	print(summary_data)
		return summary_data
		#print(raw_table_value)
	except:
		print ("Failed to parse json response")
		return {"error":"Failed to parse json response"}




if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('ticker',help = '')
	args = argparser.parse_args()
	ticker = args.ticker
	print ("Fetching data for %s"%(ticker))
	scraped_data = parse(ticker)
	print ("Writing data to output file")
	with open('%s-summary.json'%(ticker),'w') as fp:
		json.dump(scraped_data,fp,indent = 4)

PC = scraped_data.items()[0][1]
OP = scraped_data.items()[1][1]
DR = scraped_data.items()[4][1]
WR52 = scraped_data.items()[5][1]
V = scraped_data.items()[6][1]
NAV_V = scraped_data.items()[9][1]
PER = scraped_data.items()[10][1]
Y = scraped_data.items()[11][1]
D = scraped_data.items()[15][1]

print(PC,OP,DR,WR52,V,NAV_V,PER,Y,D)


#db_string = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
db_string = "postgresql://postgres:evelyn@localhost:5432/postgres"

db = create_engine(db_string)
print("a")

# Create
#db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")
db.execute("UPDATE NameFinance SET PreviousClose=OP WHERE ACTIVO='VTV'")
#, OpenPrice=scraped_data.items()[1][1], DaysRange=scraped_data.items()[4][1],WeekRange52=scraped_data.items()[5][1],Volume=scraped_data.items()[6][1], NAV=scraped_data.items()[9][1],PE_Ratio=scraped_data.items()[10][1],Yield=scraped_data.items()[11][1],ConsultDate=scraped_data.items()[15][1] WHERE Activo='%s')
print("b")
# Read
result_set = db.execute("SELECT * FROM NAmeFinance")
for r in result_set:
    print(r)

# Update
#db.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")

# Delete
#db.execute("DELETE FROM films WHERE year='2016'")
















#connection = sqlite3.connect("company.db")
#!/usr/bin/python
#engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')


#class YahooTable(object):
#    pass



#stmt = update(activos).where(Activo='%s').\
#    values(PreviousClose=scraped_data.items()[0][1])
#,OpenPrice=scraped_data.items()[1][1],DaysRange=scraped_data.items()[4][1]),WeekRange52=scraped_data.items()[5][1],Volume=scraped_data.items()[6][1],NAV=scraped_data.items()[9][1],PE Ratio = scraped_data.items()[10][1],Yield=scraped_data.items()[11][1],ConsultDate=scraped_data.items()[15][1]);
#cursor = conn.cursor()
#cursor.execute("UPDATE activos", (v1, v2, v3))
#conn.commit() # <- We MUST commit to reflect the inserted data
#cursor.close()
#conn.close()
