import urllib.request
from bs4 import BeautifulSoup as soup
import csv
import time
import random

tickers = []

g = open("comps.csv", "r")
reader = csv.reader(g)
for line in reader:
	tickers.append(line[0])

f = open("comps_ratios.csv", "a", newline="")
header = ("","EV", "EBITDA","Revenue","EBIT")
writer = csv.writer(f)
writer.writerow(header)
f.close()

for ticker in tickers:

	i_ev = -1
	i_rev = -1
	i_ebit = -1
	i_ebitda = -1

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
	str_rev = containers[i_rev].text
	str_ebit = containers[i_ebit].text
	str_ebitda = containers[i_ebitda].text

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
	str_ev = containers[i_ev].text
	
	
	# Error correcting
	if (i_rev == -1):
		str_rev = 'error'
	if (i_ebit == -1):
		str_ebit = 'error'
	if (i_ebitda == -1):
		str_ebitda = 'error'
	if (i_ev == -1):
		str_ev = 'error'
	tup = (ticker,str_ev,str_ebitda,str_rev,str_ebit)
	f = open("comps_ratios.csv", "a", newline="")
	writer = csv.writer(f)
	writer.writerow(tup)
	f.close()
	tmp = random.randint(10,15)
	print(ticker)
	time.sleep(tmp)