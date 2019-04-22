# This Python file uses the following encoding: utf-8
# import libraries
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime
import csv

# Code taken from the tutorial here https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and here https://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php

############ CONSTANTS ############

reason_code_page_url = 'https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/src/tpc/db2z_n.html?view=embed'
url_base = "https://www.ibm.com/support/knowledgecenter/SSEPEK_12.0.0/codes/"
url_view_embed = "?view=embed"

############ END CONSTANTS ############

############ FUNCTIONS ############


def soup_from_browser_and_url(browser, url):
    """This method takes a browser instance and a url. It then navigates to the page, pulls the html from it
    and parses it in to a BeautifulSoup object we can use in python to get the information from it.
    """
    # Not sure if this sleep is needed.
    # Being a good citizen during webscraping means only making 1 request per second.
    # Could maybe remove it.
    time.sleep(1)
    # navigate to the page
    browser.get(url)
    # get the pages html once the page has loaded the tags we are looking for. returns the inner HTML as a string
    page = browser.execute_script("return document.body.innerHTML")
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def reason_code_dict_from_soup(reason_code_soup):
    """This method takes a soup (A parsed html page into a python object) and extracts the reason code
    information from the page and returns it in a dictionary
    """
    # Get the info we want from the page and store it in the struct
    # Check if we find the span tag on the page because not all pages have a span tags
    span_tag = reason_code_soup.find(
        'span', class_="msgNumber")
    code_number = ""
    if span_tag:
        code_number = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'span', class_="msgText")
    msg_text = ""
    if span_tag:
        msg_text = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgExplanation")
    explanation = ""
    if span_tag:
        explanation = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgSystemAction")
    system_action = ""
    if span_tag:
        system_action = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgOperatorResponse")
    operator_response = ""
    if span_tag:
        operator_response = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgSystemProgrammerResponse")
    system_programmer_response = ""
    if span_tag:
        system_programmer_response = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgProblemDetermination")
    problem_determination = ""
    if span_tag:
        problem_determination = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgUserResponse")
    user_response = ""
    if span_tag:
        user_response = span_tag.get_text()

    span_tag = reason_code_soup.find(
        'section', class_="msgOther")
    sql_state = ""
    if span_tag:
        sql_state = span_tag.get_text()

    # Strip out newlines and unicode characters
    code_number = code_number.replace(
        "\\n", " ").encode('ascii', 'ignore')
    explanation = explanation.replace(
        "\\n", " ").encode('ascii', 'ignore')
    system_action = system_action.replace(
        "\\n", " ").encode('ascii', 'ignore')
    operator_response = operator_response.replace(
        "\\n", " ").encode('ascii', 'ignore')
    system_programmer_response = system_programmer_response.replace(
        "\\n", " ").encode('ascii', 'ignore')
    user_response = user_response.replace(
        "\\n", " ").encode('ascii', 'ignore')
    problem_determination = problem_determination.replace(
        "\\n", " ").encode('ascii', 'ignore')
    sql_state = sql_state.replace(
        "\\n", " ").encode('ascii', 'ignore')

    # Create dictionary and save to reason_code_dictionaries array
    reason_code_dict = {
        'code_number': code_number,
        'msg_text': msg_text,
        'explanation': explanation,
        'system_action': system_action,
        'operator_response': operator_response,
        'system_programmer_response': system_programmer_response,
        'user_response': user_response,
        'problem_determination': problem_determination,
        'sql_state': sql_state
    }

    return reason_code_dict

############ END FUNCTIONS ############


############ PROGRAM ############

# Program profiling. Save starting time
program_start_time = datetime.now()

# Array to store the reason code dictionaries once they have been scraped
sql_code_dictionaries = []

#### START SCRAPE ####

# replace with .Firefox(), or with the browser of your choice
browser = webdriver.Chrome('./chromedriver')
# Get the main page of the reason codes parsed into a BeautifulSoup instance
main_page_soup = soup_from_browser_and_url(browser, reason_code_page_url)

# Find all links to reason code groups
main_page_link_spans = main_page_soup.find_all(
    'span', class_="ulchildlinktext")

for span in main_page_link_spans:
    a_tag = span.find("a")
    sql_code_url = a_tag['href'].replace("../../", "")

    # Load group page and get soup
    sql_code_page = soup_from_browser_and_url(
        browser, url_base + sql_code_url + url_view_embed)
    # Parse reason code page
    sql_code_dict = reason_code_dict_from_soup(sql_code_page)

    # Append to array
    sql_code_dictionaries.append(sql_code_dict)
    print(sql_code_dict)

browser.close()

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
        code_number = '*Code Number*' + dictionary['code_number'] + '*End Code Number*'
        problem_determination = '**' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'
        problem_determination = '*Problem determination*' + dictionary['problem_determination'] + '*End Problem determination*'

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
