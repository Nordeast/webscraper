import time
import calendar
import requests
import bs4
from bs4 import BeautifulSoup
import constants
import collections
import os
import json
import math
import textwrap


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


def dict_from_soup(soup, PARSE_DICT):
    """
    This method takes a soup (A parsed html page into a python object) and extracts the information
    information from the page and returns it in a dictionary
    """
    # Get the info we want from the page and store it in the struct
    # Check if we find the span tag on the page because not all pages have a span tags

    parsed_dict = {}
    for dictionary in PARSE_DICT:
        _tag = dictionary[constants.DICT_TAG]
        _class = dictionary[constants.DICT_CLASS]

        tag = soup.find(_tag,
                        class_=_class)

        if tag:
            if dictionary[constants.DICT_CLASS] == 'msgId' or dictionary[constants.DICT_CLASS] == 'msgText':
                parsed_dict[dictionary[constants.DICT_KEY]] = [
                    {
                        'type': convert_tag_name(tag.name),
                        'content': clean_string(str(tag.get_text())),
                        'children': []
                    }
                ]
            else:
                parsed_dict[dictionary[constants.DICT_KEY]
                            ] = parse_tag(tag, None, [])
        else:
            parsed_dict[dictionary[constants.DICT_KEY]] = []

    return parsed_dict


def parse_tag(tag, parent=None, parsed_tags=[]):
    """
    Recurses down a tags tree and parses out the information.
    It represents the tree in a dictionary
    """
    text_tags = ['p', 'span', 'var', 'h1', 'h2', 'h3', 'h4', 'h5']
    for content in tag.contents:
        # Check if it is a html tag
        is_tag = type(content) is bs4.element.Tag
        # Check if it is a string
        is_string = type(
            content) is bs4.element.NavigableString and str_is_not_empty(str(content))

        # Check if a html tag that is a wrapper for a string
        is_text_tag = False
        if is_tag:
            # Can skip the section title as we have that covered
            if content.has_attr('class') and 'sectiontitle' in content['class']:
                continue
            is_text_tag = str(content.name) in text_tags

        if is_string or is_text_tag:
            # The element is just a string with no children so just get the text
            string = ''
            if is_tag:
                string = clean_string(str(content.get_text()))
            else:
                string = clean_string(str(content))

            # Skip if the string is empty
            if str_is_empty(string):
                continue

            if parent:
                # We have a parent so just add the text to the parent element
                parent['content'] = parent['content'] + string
            else:
                parsed_tags.append({
                    'type': 'string',
                    'content': string
                })
        elif is_tag:
            # If the content is a tag we need to recurse down
            # and continue parsing its children
            dictionary = {
                'type': convert_tag_name(content.name),
                'content': '',
                'children': []
            }
            parsed_tags.append(dictionary)
            parse_tag(content, dictionary, dictionary['children'])

    return parsed_tags


def clean_string(string):
    """
    Add to this method to clean the strings coming from the HTML.
    """

    string = string.replace('\n', ' ')
    string = string.replace('  ', ' ')
    string = string.encode('ascii', 'ignore').decode()
    return string


def convert_tag_name(string):
    if string == 'div':
        return 'section'
    elif string == 'ul' or string == 'dl' or string == 'ol':
        return 'list'
    elif string == 'li':
        return 'bullet'
    elif string == 'dt':
        return 'description title'
    elif string == 'dd':
        return 'description'
    elif string == 'p' or string == 'span' or string == 'var':
        return 'string'
    elif string == 'h4':
        return 'header'
    else:
        return string


def str_is_empty(string):
    return not string or string.isspace()


def str_is_not_empty(string):
    return not str_is_empty(string)


def write_soup_engine_dict_to_files(dictionaries, PARSE_DICT, file_name):
    """
    Formats and writes the dictionary out to a text file with the specified name
    and timestamp.
    """
    folder_path = os.path.join(os.getcwd(), 'Output')
    timestamp = str(calendar.timegm(time.gmtime()))

    wrapper = textwrap.TextWrapper()
    wrapper.width = constants.MAX_LINE_WIDTH
    wrapper.initial_indent = '  '
    wrapper.subsequent_indent = '  '

    index = 1
    for chunked_list in list(chunks(dictionaries, 100)):

        # Open file for writing
        output_string = ''
        for dictionary in chunked_list:
            if len(dictionary['number']) <= 0:
                continue
            code = dictionary['number'][0]['content']
            output_string += '<code> ' + code + ' <end code>'  # Parsing tags
            output_string += '\n<content>\n'  # Parsing tags

            # Write out Code
            output_string += 'Code\n'
            code_string = dictionary['number'][0]['content']

            if len(dictionary['msg_text']) > 0:
                code_string += ' ' + dictionary['msg_text'][0]['content']

            output_string += wrapper.fill(code_string)
            output_string += '\n\n'

            # Write out sections
            for key in PARSE_DICT[2:]:
                string = format_dict_to_string(
                    '', '  ', dictionary[key[constants.DICT_KEY]])
                string_len = len(string)
                if string_len > 0:
                    output_string += key[constants.DICT_DESC] + '\n'
                    output_string += string
                    output_string += '\n'

            # Write out url
            output_string += 'URL\n'
            output_string += wrapper.fill(dictionary['url'])
            output_string += '\n'

            output_string += '\n<end content>\n'  # Parsing tags

        # Remove extra new lines
        output_string = output_string.replace('\n\n\n\n\n\n\n', '\n\n')
        output_string = output_string.replace('\n\n\n\n\n\n', '\n\n')
        output_string = output_string.replace('\n\n\n\n\n', '\n\n')
        output_string = output_string.replace('\n\n\n\n', '\n\n')
        output_string = output_string.replace('\n\n\n', '\n\n')

        # Create file name
        unique_file_name = file_name + '_' + \
            str(index) + "_" + timestamp + ".txt"
        file_path = os.path.join(folder_path, unique_file_name)
        # Write string to file
        with open(file_path, 'a') as txt_file:
            txt_file.write(output_string)

        index += 1


def format_dict_to_string(string, indent, array):
    wrapper = textwrap.TextWrapper()
    wrapper.width = constants.MAX_LINE_WIDTH
    wrapper.initial_indent = indent
    wrapper.subsequent_indent = indent

    for dictionary in array:
        prefix = ''
        if dictionary['type'] == None or dictionary['content'] == 'SQLSTATE':
            continue

        if dictionary['type'] == 'bullet' or dictionary['type'] == 'description':
            prefix = '- '
            wrapper.subsequent_indent = indent + '  '

        if str_is_not_empty(dictionary['content']):
            content = prefix + dictionary['content']
            string += wrapper.fill(content) + '\n'

        if dictionary['type'] == 'code':
            string += '\n'

        if 'children' in dictionary:
            extra_indent = '  '
            if dictionary['type'] != 'list' and str_is_empty(dictionary['content']):
                extra_indent = ''

            string += format_dict_to_string('',
                                            indent + extra_indent, dictionary['children'])

        if dictionary['type'] == 'list':
            string += '\n'

    return string


def write_soup_engine_dict_to_json_files(dictionaries, file_name):
    """
    Formats and writes the dictionary out to a text file with the specified name
    and timestamp.
    """

    folder_path = os.path.join(os.getcwd(), 'Output')
    timestamp = str(calendar.timegm(time.gmtime()))

    index = 1
    for chunked_list in list(chunks(dictionaries, 100)):
        unique_file_name = file_name + '_' + \
            str(index) + "_" + timestamp + ".json"
        file_path = os.path.join(folder_path, unique_file_name)
        # Open file for writing
        with open(file_path, 'a') as json_file:
            json.dump(chunked_list, json_file, skipkeys=False, ensure_ascii=True,
                      check_circular=True, allow_nan=True, cls=None, indent=1)
        index += 1


def chunks(list, chunk_size):
    """Yield successive chunk_size'd chunks from list."""
    for i in range(0, len(list), chunk_size):
        yield list[i:i + chunk_size]
