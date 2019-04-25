# This Python file uses the following encoding: utf-8
# import libraries
from bs4 import BeautifulSoup
import time
from datetime import datetime
import soup_engine
import platform
import constants

# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

############ CONSTANTS ############

url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/n097.html?view=embed'

############ END CONSTANTS ############

############ PROGRAM ############

soup = soup_engine.soup_from_url(url)
parsed_tags = soup_engine.dict_from_soup(soup)
parsed_tags[constants.DICT_URL] = ': ' + url
soup_engine.print_soup_engine_dict(parsed_tags)
dictionaries = [parsed_tags]

soup_engine.write_soup_engine_dict_to_file(dictionaries, 'codes')
