# This Python file uses the following encoding: utf-8
# import libraries
import profiler
import soup_engine
import constants
import progress_bar

PAGE_URL = 'https://www.ibm.com/docs/en/SSEPEK_13.0.0/msgs/src/tpc/db2z_msgs.html'
URL_BASE = "https://www.ibm.com/docs/en/SSEPEK_13.0.0/msgs/"

# Program profiling. Save starting time
profiler.start()

# Get the main page of the dsn codes parsed into a BeautifulSoup instance
main_page_soup = soup_engine.soup_from_url(PAGE_URL)

# Find all links to dsn code groups
main_page_link_spans = main_page_soup.find_all(
    'li', class_="ulchildlink")

# Array for each of the dsn code pages
dsn_code_urls = []

# Progress variables
INDEX = 1
TOTAL_LENGTH = len(main_page_link_spans)
print('Scrape DSN code urls')
# Loop through main page dsn code groups
for span in main_page_link_spans:
    a_tag = span.find("a")
    group_url = a_tag['href'].replace("../../", "")

    # Load group page and get soup
    child_page_soup = soup_engine.soup_from_url(
        URL_BASE + group_url)

    # Get the links to the individual code pages
    child_page_link_spans = child_page_soup.find_all(
        'li', class_="ulchildlink")

    for span in child_page_link_spans:
        a_tag = span.find("a")
        dsn_code_url = a_tag['href'].replace("../../", "")
        url = URL_BASE + dsn_code_url
        dsn_code_urls.append(url)

    progress_bar.print(INDEX, TOTAL_LENGTH, 'Progress',
                       '(' + str(INDEX) + '/' + str(TOTAL_LENGTH) + ') URLs Scraped')
    INDEX += 1

# Array to store the dsn code dictionaries once they have been scraped
dsn_code_dictionaries = []
INDEX = 1
TOTAL_LENGTH = len(dsn_code_urls)
print('Scrape Pages')
# Scrape the dsn code pages=
for url in dsn_code_urls:
    # Load group page and get soup
    soup = soup_engine.soup_from_url(url)
    # Parse code page
    parsed_tags = soup_engine.dict_from_soup(soup, constants.PARSE_DICT)
    parsed_tags[constants.DICT_URL] = url
    # Append to array
    dsn_code_dictionaries.append(parsed_tags)

    progress_bar.print(INDEX, TOTAL_LENGTH, 'Progress',
                       '(' + str(INDEX) + '/' + str(TOTAL_LENGTH) + ') Pages Scraped')
    INDEX += 1


# Write to file
FILE_NAME = 'dsn_codes'
print('Writing parsed codes to file with name ' + FILE_NAME)
soup_engine.write_soup_engine_dict_to_files(
    dsn_code_dictionaries, constants.PARSE_DICT, FILE_NAME)

profiler.end()
