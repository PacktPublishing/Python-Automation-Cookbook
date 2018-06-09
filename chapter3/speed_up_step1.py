import argparse
import requests
import logging
import http.client
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import concurrent.futures

URL = 'https://www.cs.vu.nl/~ast/'
DEFAULT_PHRASE = 'scientist'


def process_link(source_link, text):
    logging.info(f'Extracting links from {source_link}')
    parsed_source = urlparse(source_link)
    result = requests.get(source_link)
    if result.status_code != http.client.OK:
        logging.error(f'Error retrieving {source_link}: {result}')
        return source_link, []

    if 'html' not in result.headers['Content-type']:
        logging.info(f'Link {source_link} is not an HTML page')
        return source_link, []

    page = BeautifulSoup(result.text, 'html.parser')
    search_text(source_link, page, text)

    return source_link, get_links(parsed_source, page)


def get_links(parsed_source, page):
    '''Retrieve the links on the page'''
    links = []
    for element in page.find_all('a'):
        link = element.get('href')
        if not link:
            continue

        if parsed_source.netloc not in link:
            continue

        # Check that the link is a valid reference link
        if not link.startswith('http'):
            continue

        links.append(link)

    return links


def search_text(source_link, page, text):
    '''Search for an element with the searched text and print it'''
    for element in page.find_all(text=re.compile(text)):
        print(f'Link {source_link}: --> {element}')


def main(base_url, to_search, workers):
    checked_links = set()
    to_check = [base_url]
    max_checks = 10

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        while to_check:
            futures = [executor.submit(process_link, url, to_search)
                       for url in to_check]
            to_check = []
            for data in concurrent.futures.as_completed(futures):
                link, new_links = data.result()

                checked_links.add(link)
                for link in new_links:
                    if link not in checked_links and link not in to_check:
                        to_check.append(link)

                max_checks -= 1
                if not max_checks:
                    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, help='Base site url',
                        default=URL)
    parser.add_argument('-p', type=str, help='Sentence to search',
                        default=DEFAULT_PHRASE)
    parser.add_argument('-w', type=int, help='Number of workers',
                        default=4)
    args = parser.parse_args()

    main(args.u, args.p, args.w)
