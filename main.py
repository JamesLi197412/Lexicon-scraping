from scraping import *
from parsing import *


def task(filename):
    # Task 1 : Find out latest version
    web_url = version_scraping()

    # Task 2: Find the XML File url
    xml_url = find_xml(web_url)

    # Task 3: Download the file
    load_xml(xml_url, filename)

    # Task 4: Parse XML file and return local file
    parse_xml(filename)


if __name__ == '__main__':
    task('LEXICON.xml')

