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
# TODO URLS
# https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/n181.html

url = 'https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.1.0/com.ibm.zos.v2r1.ieam800/gg278i.htm'

add_embed = True
if add_embed:
    url = url + '?view=embed'

PARSE_DICT = constants.SYSTEM_MESSAGES_PARSE_DICT

############ END CONSTANTS ############

############ PROGRAM ############

soup = soup_engine.soup_from_url(url)
parsed_tags = soup_engine.dict_from_soup(soup, PARSE_DICT)
parsed_tags[constants.DICT_URL] = url
dictionaries = [parsed_tags]
soup_engine.write_soup_engine_dict_to_files(
    dictionaries, PARSE_DICT, 'codes')
soup_engine.write_soup_engine_dict_to_json_files(dictionaries, 'codes')
