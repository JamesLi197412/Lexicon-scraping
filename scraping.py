import requests
from bs4 import BeautifulSoup

def find_xml(url):
    """

    :param url: latest version of file
    :return: XML href link
    """
    soup = get_page(url)

    # Find the target Link: XML
    page = soup.find("div", {'class': "container padding-top-4 padding-bottom-4"})
    data = page.find('ul').find_all('li')

    for element in data:
        if 'xml' in element.text:
            lenght = 1000
            if len(element.text) < lenght:
                texts = element.text
                link = element.a.get('href')

    return link

def version_scraping():
    """
        With specific URL, find out latest version of data
    """
    link = 'https://lhncbc.nlm.nih.gov/LSG/Projects/lexicon/current/web/release/index.html'
    soup_bs = get_page(link)

    # Find the latest version
    page = soup_bs.find("div", {'class': "container padding-top-4 padding-bottom-4"})
    results = page.find('ul')

    # dict to store version and compare
    versions = dict()
    for li in results.find_all("li"):
        # preprocess the href
        href = li.a.get('href')
        if (len(href) < 20):
            href = href[2:]
            href = 'https://lhncbc.nlm.nih.gov/LSG/Projects/lexicon/current/web/release/' + href

        # preprocess the context
        context = li.text
        context = context.split('\n')[0]

        versions[context] = href

    index = return_latest_index(versions)
    new_url =  versions[index]

    return new_url


def return_latest_index(dictionary):
    keys = list(dictionary.keys())
    years = [int(key.split(' ')[0]) for key in keys]
    indexs = years.index(max(years))

    return keys[indexs]


def get_page(url):
    """

    :param url: url to explore
    :return: beautiful soup for exploring the web page
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application'
                  '/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print(response.text)  # Print the content of the response
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f'Request failed with status code: {response.status_code}')
        return None



