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

f = open("ratios.csv", "a", newline="")
header = ("","PE","Revenue","EBIT","EBITDA","EV", "Cash", "Debt", "Diluted S/O")
writer = csv.writer(f)
writer.writerow(header)
f.close()

for ticker in tickers:

	i_pe = -1
	i_rev = -1
	i_ebit = -1
	i_ebitda = -1
	i_ev = -1
	i_cash = -1
	i_debt = -1
	i_so = -1

	# INCOME STATEMENT
	my_url = 'https://stockanalysis.com/stocks/' + ticker + '/financials/'
	uClient = urllib.request.Request(my_url, headers = {'User-Agent': 'Mozilla/5.0'})
	uClient = urllib.request.urlopen(uClient)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("td")
	for i in range(0, len(containers)):
		if (containers[i].text == 'Revenue'):
			i_rev = i + 1
		elif (containers[i].text == 'EBIT'):
			i_ebit = i + 1
		elif (containers[i].text == 'EBITDA'):
			i_ebitda = i + 1
		elif (containers[i].text == 'Shares Outstanding (Diluted)'):
			i_so = i + 1
	str_rev = containers[i_rev].text
	str_ebit = containers[i_ebit].text
	str_ebitda = containers[i_ebitda].text
	str_so = containers[i_so].text


	# BALANCE SHEET
	my_url = 'https://stockanalysis.com/stocks/' + ticker + '/financials/balance-sheet/'
	uClient = urllib.request.Request(my_url, headers = {'User-Agent': 'Mozilla/5.0'})
	uClient = urllib.request.urlopen(uClient)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("td")
	for i in range(0, len(containers)):
		if (containers[i].text == 'Cash & Cash Equivalents'):
			i_cash = i + 1
		elif (containers[i].text == 'Total Debt'):
			i_debt = i + 1
	str_cash = containers[i_cash].text
	str_debt = containers[i_debt].text


	# RATIOS
	my_url = 'https://stockanalysis.com/stocks/' + ticker + '/financials/ratios/'
	uClient = urllib.request.Request(my_url, headers = {'User-Agent': 'Mozilla/5.0'})
	uClient = urllib.request.urlopen(uClient)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("td")
	for i in range(0, len(containers)):
		if (containers[i].text == 'Enterprise Value'):
			i_ev = i + 1
		elif (containers[i].text == 'PE Ratio'):
			i_pe = i + 1
	str_pe = containers[i_pe].text
	str_ev = containers[i_ev].text
	
	
	# Error correcting
	if (i_pe == -1):
		str_pe = 'error'
	if (i_rev == -1):
		str_rev = 'error'
	if (i_ebit == -1):
		str_ebit = 'error'
	if (i_ebitda == -1):
		str_ebitda = 'error'
	if (i_ev == -1):
		str_ev = 'error'
	if (i_cash == -1):
		str_cast = 'error'
	if (i_debt == -1):
		str_debt = 'error'
	if (i_so == -1):
		str_so = 'error'
	tup = (ticker,str_pe,str_rev,str_ebit,str_ebitda,str_ev,str_cash,str_debt,str_so)
	f = open("ratios.csv", "a", newline="")
	writer = csv.writer(f)
	writer.writerow(tup)
	f.close()
	tmp = random.randint(10,15)
	print(ticker)
	time.sleep(tmp)