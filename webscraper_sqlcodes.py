# This Python file uses the following encoding: utf-8
# import libraries
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv
import soup_engine
import platform

# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

############ CONSTANTS ############

reason_code_page_url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/db2z_n.html?view=embed'
url_base = "https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/"
url_view_embed = "?view=embed"

############ END CONSTANTS ############

############ PROGRAM ############

# Program profiling. Save starting time
program_start_time = datetime.now()

# Array to store the reason code dictionaries once they have been scraped
sql_code_dictionaries = []

#### START SCRAPE ####

# Get the main page of the reason codes parsed into a BeautifulSoup instance
main_page_soup = soup_engine.soup_from_url(reason_code_page_url)

# Find all links to reason code groups
main_page_link_spans = main_page_soup.find_all(
    'span', class_="ulchildlinktext")

for span in main_page_link_spans:
    a_tag = span.find("a")
    sql_code_url = a_tag['href'].replace("../../", "")

    # Load group page and get soup
    sql_code_page = soup_engine.soup_from_url(
        url_base + sql_code_url + url_view_embed)
    # Parse reason code page
    sql_code_dict = soup_engine.dict_from_soup(
        sql_code_page)

    # Append to array
    sql_code_dictionaries.append(sql_code_dict)
    print(sql_code_dict)

#### END SCRAPE ####

#### WRITE TO CSV ####

# Write dictionaries to csv
csv_name = "sql_codes_" + datetime.now().replace(microsecond=0).isoformat() + ".csv"
with open(csv_name, 'w') as csv_file:
    writer = csv.writer(csv_file)
    # Heading row
    writer.writerow(['code_number', 'msg_text', 'explanation',
                     'system_action', 'operator_response', 'system_programmer_response', 'user_response', 'problem_determination', 'sql_state'])

    # Loop through dictionaries and write a csv row for each
    for dictionary in sql_code_dictionaries:
        code_number = '*Code Number*' + \
            dictionary['code_number'] + '*End Code Number*'
        problem_determination = '**' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + \
            dictionary['problem_determination'] + '*End Problem determination*'

        writer.writerow('*Start Page*',
                        [dictionary['code_number'],
                         dictionary['msg_text'],
                         dictionary['explanation'],
                         dictionary['system_action'],
                         dictionary['operator_response'],
                         dictionary['system_programmer_response'],
                         dictionary['user_response'],
                         dictionary['problem_determination'],
                         dictionary['sql_state']],
                        '*End Page*')

print("csv written with name: " + csv_name)

#### END WRITE TO CSV ####

# print how long the program took to run
program_duration = datetime.now() - program_start_time
seconds = program_duration.seconds
hours, remainder = divmod(seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print("Time to complete:")
print('{:02}:{:02}:{:02} HH:MM:SS'.format(
    int(hours), int(minutes), int(seconds)))

############ END PROGRAM ############
