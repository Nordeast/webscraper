import time
import requests
import bs4
from bs4 import BeautifulSoup
import constants

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
    """This method takes a soup (A parsed html page into a python object) and extracts the information
    information from the page and returns it in a dictionary
    """
    # Get the info we want from the page and store it in the struct
    # Check if we find the span tag on the page because not all pages have a span tags

    parsed_dict = {}
    for dictionary in constants.PARSE_DICT:
        tag = soup.find(dictionary[constants.DICT_TAG], class_=dictionary[constants.DICT_CLASS])
        if tag:
            parsed_dict[dictionary[constants.DICT_KEY]] = parse_tag(tag)
        else:
            parsed_dict[dictionary[constants.DICT_KEY]] = []

    return parsed_dict

def parse_tag(tag, spacing='', parsed_tags=[]):
    for content in tag.contents:
        if type(content) is bs4.element.Tag:
            if spacing:
                parse_tag(content, spacing + ' > ' + content.name, parsed_tags)
            else:
                parse_tag(content, content.name, parsed_tags)
        elif type(content) is bs4.element.NavigableString and not str(content).isspace():
            parsed_tag = spacing + ': ' + str(content).replace('\n', ' ')
            parsed_tags.append(parsed_tag)
            # print(parsed_tag)
    return parsed_tags

def print_soup_engine_dict(dictionary):
    for parse_dict in constants.PARSE_DICT:
        array_to_print = dictionary[parse_dict[constants.DICT_KEY]]
        print(parse_dict[constants.DICT_KEY])
        for string in array_to_print:
            print('    ' + string)