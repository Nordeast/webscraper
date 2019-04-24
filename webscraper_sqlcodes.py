# This Python file uses the following encoding: utf-8
# import libraries
from bs4 import BeautifulSoup
import soup_engine
import profile
import constants

# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

page_url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/db2z_n.html?view=embed'
url_base = "https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/"
url_view_embed = "?view=embed"

############ PROGRAM ############

# Program profiling
profile.start()

# Array to store the reason code dictionaries once they have been scraped
sql_code_dictionaries = []

#### START SCRAPE ####

# Get the main page of the reason codes parsed into a BeautifulSoup instance
main_page_soup = soup_engine.soup_from_url(page_url)

# Find all links to reason code groups
main_page_link_spans = main_page_soup.find_all(
    'span', class_="ulchildlinktext")

for span in main_page_link_spans:
    a_tag = span.find("a")
    sql_code_url = a_tag['href'].replace("../../", "")

    # Load group page and get soup
    url = url_base + sql_code_url
    soup = soup_engine.soup_from_url(url + url_view_embed)
    # Parse code page
    parsed_tags = soup_engine.dict_from_soup(soup)
    parsed_tags[constants.DICT_URL] = ': ' + url
    # Print results to console
    soup_engine.print_soup_engine_dict(parsed_tags)
    # Append to array
    sql_code_dictionaries.append(parsed_tags)

#### END SCRAPE ####

# End Program profiling
profile.end()

############ END PROGRAM ############
