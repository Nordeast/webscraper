import time
from datetime import datetime
import requests
import bs4
from bs4 import BeautifulSoup
import constants
import collections
import os


def soup_from_url(url):
    """This method takes a browser instance and a url. It then navigates to the page, pulls the html from it
    and parses it in to a BeautifulSoup object we can use in python to get the information from it.
    """

    # Being a good citizen during webscraping means only making 1 request per second.
    time.sleep(1)
    # Get page from url
    response = requests.get(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def dict_from_soup(soup):
    """
    This method takes a soup (A parsed html page into a python object) and extracts the information
    information from the page and returns it in a dictionary
    """
    # Get the info we want from the page and store it in the struct
    # Check if we find the span tag on the page because not all pages have a span tags

    parsed_dict = {}
    for dictionary in constants.PARSE_DICT:
        tag = soup.find(dictionary[constants.DICT_TAG],
                        class_=dictionary[constants.DICT_CLASS])
        if tag:
            parsed_dict[dictionary[constants.DICT_KEY]
                        ] = parse_tag(tag, '', [])
        else:
            parsed_dict[dictionary[constants.DICT_KEY]] = []

    return parsed_dict


def parse_tag(tag, spacing='', parsed_tags=[]):
    """ 
    Recurses down a tags tree and parses out the information.
    It represents the tree by element > child element : content
    """
    for content in tag.contents:
        if type(content) is bs4.element.Tag:
            carrot = ''
            if spacing:
                carrot = ' > '
            # If the content is a tag we need to recurse down
            # and find its content
            parse_tag(content, spacing + carrot + content.name, parsed_tags)
        elif type(content) is bs4.element.NavigableString and not str(content).isspace():
            # Content was a string so we need to grab its content
            parsed_tag = spacing + ': ' + clean_string(str(content))
            parsed_tags.append(parsed_tag)
    return parsed_tags


def clean_string(string):
    """ 
    Add to this method to clean the strings coming from the HTML.
    """

    string = string.replace('\n', ' ')
    string = string.replace('  ', ' ')
    string = string.strip()
    return string


def print_soup_engine_dict(dictionary):
    """ 
    This method is for debugging purposes. It takes a dict_from_soup dictionary
    and pretty prints it to the console.
    """

    print('<<<<<<<<<<>>>>>>>>>>')
    print('')
    for parse_dict in constants.PARSE_DICT:
        value = dictionary[parse_dict[constants.DICT_KEY]]
        print(parse_dict[constants.DICT_KEY])
        for string in value:
            print('    ' + string)

    print(constants.DICT_URL)
    print('    ' + dictionary[constants.DICT_URL])
    print('')
    print('<<<<<<<<<<>>>>>>>>>>')


def write_soup_engine_dict_to_file(dictionaries, file_name):
    """
    Formats and writes the dictionary out to a text file with the specified name
    and timestamp.
    """
    # Create file name and path
    file_name = file_name + '_' + \
        datetime.now().replace(microsecond=0).isoformat() + ".txt"
    file_path = os.path.join('./Output_Files', file_name)
    # Open file for writing
    with open(file_path, 'a') as txt_file:
        # Begin looping and writing to the file
        for dictionary in dictionaries:
            txt_file.write('**start section**\n')
            for parse_dict in constants.PARSE_DICT:
                value = dictionary[parse_dict[constants.DICT_KEY]]
                txt_file.write(parse_dict[constants.DICT_KEY] + '\n')
                for string in value:
                    txt_file.write('    ' + string + '\n')

            txt_file.write(constants.DICT_URL + '\n')
            txt_file.write('    ' + dictionary[constants.DICT_URL] + '\n')
            txt_file.write('**end section**\n')
