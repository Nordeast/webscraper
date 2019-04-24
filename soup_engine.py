import time
import requests
import bs4
from bs4 import BeautifulSoup


def soup_from_url(url):
    """This method takes a browser instance and a url. It then navigates to the page, pulls the html from it
    and parses it in to a BeautifulSoup object we can use in python to get the information from it.
    """
    # Not sure if this sleep is needed.
    # Being a good citizen during webscraping means only making 1 request per second.
    # Could maybe remove it.
    time.sleep(1)
    # Get page from url
    response = requests.get(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def dict_from_soup(soup):
    """This method takes a soup (A parsed html page into a python object) and extracts the reason code
    information from the page and returns it in a dictionary
    """
    # Get the info we want from the page and store it in the struct
    # Check if we find the span tag on the page because not all pages have a span tags
    span_tag = soup.find(
        'span', class_="msgNumber")
    code_number = ""
    if span_tag:
        code_number = span_tag.get_text()

    span_tag = soup.find(
        'span', class_="msgText")
    msg_text = ""
    if span_tag:
        msg_text = span_tag.get_text()

    span_tag = soup.find(
        'section', class_="msgExplanation")
    explanation = ""
    if span_tag:
        explanation = span_tag.get_text()

    span_tag = soup.find(
        'section', class_="msgSystemAction")
    system_action = ""
    if span_tag:
        system_action = span_tag.get_text()

    span_tag = soup.find(
        'section', class_="msgOperatorResponse")
    operator_response = ""
    if span_tag:
        operator_response = span_tag.get_text()

    span_tag = soup.find(
        'section', class_="msgSystemProgrammerResponse")
    system_programmer_response = ""
    if span_tag:
        system_programmer_response = span_tag.get_text()

    span_tag = soup.find(
        'section', class_="msgProblemDetermination")
    problem_determination = ""
    if span_tag:
        problem_determination = span_tag.get_text()

    span_tag = soup.find(
        'section', class_="msgUserResponse")
    user_response = ""
    if span_tag:
        user_response = span_tag.get_text()

    span_tag = soup.find(
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


def parse(soup):
    for child in soup.find('section', class_="msgExplanation").children:
        going(child, '')


def going(tag, spacing):
    if type(tag) is bs4.element.Tag:
        if tag.name == 'ul':
            print_and_continue(tag, 'ul', spacing + ' ul')
        elif tag.name == 'div':
            print_and_continue(tag, 'div', spacing + ' div')
        elif tag.name == 'li':
            print_and_continue(tag, 'li', spacing + ' li')
        elif tag.name == 'p':
            print_and_continue(tag, 'p', spacing + ' p')
        elif tag.name == 'span':
            print_and_continue(tag, 'span', spacing + ' span')
    return


def print_and_continue(tag, element, spacing):
    for content in tag.contents:
        if type(content) is bs4.element.NavigableString:
            if unicode(content) != '\n':
                print(spacing + ' ' +
                      unicode(content).replace('\n', ' '))
        elif type(tag) is bs4.element.Tag:
            going(content, spacing)
