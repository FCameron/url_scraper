import urllib.request
from bs4 import BeautifulSoup as soup
import csv
import time
import random

tickers = []

g = open("tickers.csv", "r")
reader = csv.reader(g)
for line in reader:
	tickers.append(line[0])

f = open("test.csv", "a", newline="")
header = ("","2020","2019","2018","2017","2016", "cash", "Long-Term Debt")
writer = csv.writer(f)
writer.writerow(header)
f.close()

for ticker in tickers:
	my_url = 'https://stockanalysis.com/stocks/' + ticker + '/financials/'
	uClient = urllib.request.Request(my_url, headers = {'User-Agent': 'Mozilla/5.0'})
	uClient = urllib.request.urlopen(uClient)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	str1 = []
	containers = page_soup.findAll("td")

	index0 = -1
	for i in range(0, len(containers)):
		if (containers[i].text == 'EPS (Diluted)'):
			index0 = i + 1
	print(ticker)
	str1.append(containers[index0].text)
	str1.append(containers[index0+1].text)
	str1.append(containers[index0+2].text)
	str1.append(containers[index0+3].text)
	str1.append(containers[index0+4].text)

	my_url = 'https://stockanalysis.com/stocks/' + ticker + '/financials/balance-sheet/'
	uClient = urllib.request.Request(my_url, headers = {'User-Agent': 'Mozilla/5.0'})
	uClient = urllib.request.urlopen(uClient)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("td")

	str2 = []
	index1 = -1
	index2 = -1
	for i in range(0, len(containers)):
		if (containers[i].text == 'Cash & Cash Equivalents'):
			index1 = i + 1
		elif (containers[i].text == 'Total Liabilities'):
			index2 = i + 1

	str2.append(containers[index1].text)
	str2.append(containers[index2].text)
	if (index1 == -1): 
		str2[0] = 'Error'
	if (index2 == -1): 
		str2[1] = 'Error'
	tup = (ticker,str1[0],str1[1],str1[2],str1[3],str1[4], str2[0],str2[1])
	f = open("test.csv", "a", newline="")
	writer = csv.writer(f)
	writer.writerow(tup)
	f.close()
	tmp = random.randint(10,15)
	time.sleep(tmp)

f = open("test.csv", "a", newline="")
writer = csv.writer(f)
for tup1 in tup:
	writer.writerow(tup1)
f.close()