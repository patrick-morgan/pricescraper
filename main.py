import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession
import os
import numpy as np

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver_path = os.getcwd() + "/chromedriver"

driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
driver.get('http://www.google.com/')

query = input("What item would you like to look up today? ")
print(f"\nSearching for {query}")

# Get input ready for url search
query = query.replace(' ', '+')

# Scrape top result from ebay
url_ebay = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=" + query
webpage = requests.get(url_ebay)
soup = BeautifulSoup(webpage.content, "html.parser")
results = soup.find(id='mainContent')
listings = results.find_all('li', class_='s-item')

runs = 0
for listing in listings:
    if runs>=1: break
    item_element = listing.find('h3', class_='s-item_title')
    item_price = listing.find('span', class_='s-item__price')
    if None in (item_element, item_price):
        continue
    runs += 1
ebay_price = float(item_price.text.strip().replace('$', ''))

# Scrape top result from Amazon
url_amazon = "https://www.amazon.com/s?k=" + query
driver.get(url_amazon)
soup = BeautifulSoup(driver.page_source, 'html.parser')

runs = 0
results = soup.findAll('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
for listing in results:
    if runs >= 1: break
    soup.select_one('span.a-size-medium').get_text()
    runs += 1

runs = 0
results = soup.findAll('span', attrs={'class': 'a-offscreen'})
for listing in results:
    if runs >= 1: break
    element = soup.select_one('span.a-offscreen')
    if None in element:
        continue
    runs += 1

# save price
amazon_price = float(element.text.strip().replace('$', ''))


bb_price = 10323929.32
if ebay_price < amazon_price:
    elected_price = ebay_price
    elected_link = url_ebay
else:
    elected_price = amazon_price
    elected_link = url_amazon


print(elected_price)
print(elected_link)
driver.quit()