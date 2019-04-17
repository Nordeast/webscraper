# This Python file uses the following encoding: utf-8
# import libraries
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

# url for the reason codes
reason_code_page_url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_11.0.0/codes/src/tpc/db2z_reasoncodes.html?view=embed'
url_base = "https://www.ibm.com/support/knowledgecenter/SSEPEK_11.0.0/codes/"
url_view_embed = "?view=embed"

# replace with .Firefox(), or with the browser of your choice
browser = webdriver.Chrome('./chromedriver')
browser.get(reason_code_page_url)  # navigate to the page

# get the pages html once the page has loaded the tags we are looking for. returns the inner HTML as a string
page = browser.execute_script("return document.body.innerHTML")

# this code will write the html out to its own file for your viewing
# file = open("reasoncodes.html", "w")
# file.write(page.encode('utf-8'))

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

all_link_span_tags = soup.find_all('span', class_="ulchildlinktext")

# get our list of urls from the main page
reason_code_page_urls = []
for span in all_link_span_tags:
    a_tag = span.find_all("a")
    reason_code_page_urls.append(a_tag[0]['href'].replace("../../", ""))


browser.get(url_base + reason_code_page_urls[0] + url_view_embed)
