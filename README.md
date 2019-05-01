# Webscraper

This project scrapes the reason and SQL codes off of the IBM website and outputs them into a JSON document perserving the formatting of the HTML.

The script takes about 23 mins to scrape and parse the SQL codes and about an hour for the reason codes.

## Requirements
- python 3.7.+

## Dependencies
- requests
- BeautifulSoup4

To install the dependecies use `pip install requests` and `pip install beautifulSoup4`.

## Runing the scripts
You can run the scripts from the command line or there are configurations to debug them from Visual Studio Code.

### Visual Studio Code
Clone this repository and open it in Visual Studio Code. On the left hand side hit the debug tab and choose the configuration at the top. Then press the green run button or `F5` keyboard shortcut.

![Visual Studio Code Screenshot](https://raw.githubusercontent.com/nordeast/webscraper/master/Images/screenshot1.png)

### Command Line
- `python reason_codes.py`
parses the reason codes
- `python sql_codes.py`
parses the SQL codes
- `python working.py`
simpler script that leverages all the functionality but only scrapes one reason/SQL code on outputs it to a JSON document
- `python parse_and_print.py`
simpler script that leverages all the functionality but only scrapes one reason/SQL code and pretty prints it to the console
