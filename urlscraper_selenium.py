from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import csv
import time
import random

tickers = []

g = open("tickers.csv", "r")
reader = csv.reader(g)
for line in reader:
	tickers.append(line[0])

f = open("quick_comps.csv", "a", newline="")
header = ("target","comps")
writer = csv.writer(f)
writer.writerow(header)
f.close()

quick_comps_list = []

PATH = "path_to_chromedriver_here"
driver = webdriver.Chrome(PATH)

username = ""
password = ""

wait = WebDriverWait(driver, 15)
driver.get("https://www.capitaliq.com")
quick_comps = wait.until(presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
search_tab = wait.until(presence_of_element_located((By.ID, "SearchTopBar")))
for ticker in tickers:
	time.sleep(random.randint(5,10))
	try:
		driver.find_element(By.ID, "SearchTopBar").send_keys(":" + ticker)
		time.sleep(random.randint(2,7))
		driver.find_element(By.ID, "SearchTopBar").send_keys( Keys.ARROW_DOWN + Keys.RETURN)
		quick_comps = wait.until(presence_of_element_located((By.ID, "ll_7_26_2305")))
		link = driver.find_element(By.LINK_TEXT, "Quick Comps")
		link.click()
		companies = wait.until(presence_of_element_located((By.CLASS_NAME, "noUnderLine")))
		quick_comps_list = driver.find_elements(By.CLASS_NAME, "noUnderLine")
		print(ticker + " success")
	except:
		quick_comps_list = []
		print(ticker + " failure")
	comps_list = ()
	comps_list += (ticker,)
	for comp in quick_comps_list:
		comps_list += (comp.text,)
	f = open("quick_comps.csv", "a", newline="")
	writer = csv.writer(f)
	writer.writerow(comps_list)
	f.close()
print(quick_comps_list)
for comp in quick_comps_list:
	print(comp.text)
driver.quit()