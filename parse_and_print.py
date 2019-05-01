# This Python file uses the following encoding: utf-8
# import libraries
from bs4 import BeautifulSoup
import time
from datetime import datetime
import soup_engine
import platform
import constants
import json
# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

############ CONSTANTS ############

url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/n159.html'

add_embed = True
if add_embed:
    url = url + '?view=embed'

############ END CONSTANTS ############

def print_section(section, spacing=''):
    # Begin looping and writing to the file
    if section is None:
        return

    for item in section:
        item_type = item.get('type', None)
        item_content = item.get('content', None)
        item_children = item.get('children', None)
        
        prefix = ''
        if item_type == 'bullet':
            prefix = '- '
        elif item_type == 'description title':
            prefix = ''
        elif item_type == 'description':
            prefix = '  '
        elif item_type == 'h4':
            prefix = ''

        if item_content:
            print(spacing + prefix + item_content)

        print_section(item_children, spacing + '  ')


############ PROGRAM ############

soup = soup_engine.soup_from_url(url)
parsed_tags = soup_engine.dict_from_soup(soup)
parsed_tags[constants.DICT_URL] = url
dictionaries = [parsed_tags]

for dictionary in dictionaries:
    print('**start section**')
    
    for parse_dict in constants.PARSE_DICT:
        section_array = dictionary[parse_dict[constants.DICT_KEY]]
        if parse_dict[constants.DICT_KEY] == constants.DICT_URL:
            print(section_array)
        else:
            print_section(section_array)
        
    print('**end section**')


