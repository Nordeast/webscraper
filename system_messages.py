# This Python file uses the following encoding: utf-8
# import libraries
from bs4 import BeautifulSoup
import soup_engine
import profiler
import constants
import progress_bar

# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

urls = [
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-ief-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iefa-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iefah-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iefc-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iefe-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iefi-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iefj-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-ieh-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iew-messages-iew0000-iew0999',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iew-messages-iew1001-iew1999',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iew-messages-iew2001-iew2999',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iew-messages-iew3000-iew3999',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iew-messages-iew4000-iew4999',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-iew-messages-iew5000-iew5057',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-ifa-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-ifb-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-ifc-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-messages',
    'https://www.ibm.com/docs/en/zos/3.1.0?topic=igd-igdh-messages'
]

URL_BASE = "https://www.ibm.com/docs/en/SSLTBW_3.1.0/com.ibm.zos.v3r1.ieam800/"

PARSE_DICT = constants.SYSTEM_MESSAGES_PARSE_DICT

############ PROGRAM ############

# Program profiling
profiler.start()

# Array to store the reason code dictionaries once they have been scraped
parsed_dictionaries = []
child_urls = []

#### START SCRAPE ####
for link in urls:
    print('Scraping: ' + link)

    # Get the main page of the reason codes parsed into a BeautifulSoup instance
    main_page_soup = soup_engine.soup_from_url(link)
    # Find all links to reason code groups
    main_page_link_list_items = main_page_soup.find_all(
        'li', class_="ulchildlink")

    for list_item in main_page_link_list_items:
        a_tag = list_item.find("a")
        parsed_url = a_tag['href'].replace("../../", "")
        parsed_url = parsed_url.split('#', 1)[0]

        # Load group page and get soup
        child_urls.append(URL_BASE + parsed_url)

INDEX = 1
TOTAL_LENGTH = len(child_urls)
for url in child_urls:
    soup = soup_engine.soup_from_url(url)
    # Parse code page
    parsed_tags = soup_engine.dict_from_soup(soup, PARSE_DICT)
    parsed_tags[constants.DICT_URL] = url
    # Append to array
    parsed_dictionaries.append(parsed_tags)

    progress_bar.print(INDEX, TOTAL_LENGTH, 'Progress',
                        '(' + str(INDEX) + '/' + str(TOTAL_LENGTH) + ') Pages Scraped')
    INDEX += 1

# Write to file
FILE_NAME = 'system_messages'
print('Writing parsed pages to file with name ' + FILE_NAME)
soup_engine.write_soup_engine_dict_to_files(
    parsed_dictionaries, PARSE_DICT, FILE_NAME)

#### END SCRAPE ####

# End Program profiling
profiler.end()

############ END PROGRAM ############
