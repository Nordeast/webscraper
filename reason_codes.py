# This Python file uses the following encoding: utf-8
# import libraries
from bs4 import BeautifulSoup
import soup_engine
import profile
import constants
import progress_bar

page_url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/db2z_reasoncodes.html?view=embed'
url_base = "https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/"
url_view_embed = "?view=embed"

# Program profiling. Save starting time
profile.start()

# Get the main page of the reason codes parsed into a BeautifulSoup instance
main_page_soup = soup_engine.soup_from_url(page_url)

# Find all links to reason code groups
main_page_link_spans = main_page_soup.find_all(
    'span', class_="ulchildlinktext")

# Array for each of the reason code pages
reason_code_urls = []

# Progress variables
index = 1
total_length = len(main_page_link_spans)
print('Scrape Reason code urls')
# Loop through main page reason code groups
for span in main_page_link_spans:
    a_tag = span.find("a")
    group_url = a_tag['href'].replace("../../", "")

    # Load group page and get soup
    child_page_soup = soup_engine.soup_from_url(url_base + group_url + url_view_embed)

    # Get the links to the individual code pages
    child_page_link_spans = child_page_soup.find_all(
        'span', class_="ulchildlinktext")

    for span in child_page_link_spans:
        a_tag = span.find("a")
        reason_code_url = a_tag['href'].replace("../../", "")
        url = url_base + reason_code_url
        reason_code_urls.append(url)

    progress_bar.print(index, total_length, 'Progress',
                    '(' + str(index) + '/' + str(total_length) + ') URLs Scraped')
    index += 1
        
# Array to store the reason code dictionaries once they have been scraped
reason_code_dictionaries = []
index = 1
total_length = len(reason_code_urls)
print('Scrape Pages')
# Scrape the reason code pages=
for url in reason_code_urls:
    # Load group page and get soup
    soup = soup_engine.soup_from_url(url + url_view_embed)
    # Parse code page
    parsed_tags = soup_engine.dict_from_soup(soup)
    parsed_tags[constants.DICT_URL] = ': ' + url
    # Append to array
    reason_code_dictionaries.append(parsed_tags)

    progress_bar.print(index, total_length, 'Progress',
                       '(' + str(index) + '/' + str(total_length) + ') Pages Scraped')
    index += 1


# Write to file
file_name = 'reason_codes'
print('Writing parsed codes to file with name ' + file_name)
soup_engine.write_soup_engine_dict_to_file(reason_code_dictionaries, file_name)

profile.end()