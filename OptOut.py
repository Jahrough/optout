import argparse
import requests
import re
from bs4 import BeautifulSoup


class OptOut:
    def __init__(self, name):
        self.name = name
        self.page_count = 0
        self.links = []
        self.sites = [
            'clustrmap',
            'mylife',
            'fastpeoplesearch'
        ]

    def get_page_html(self):
        url = 'https://www.google.com/search?q={0}&start={1}'.format(self.name, self.page_count)
        response = requests.get(url)
        if response.ok and response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception('Received status code {0} when trying to retrieve a response from "{1}"'
                            .format(response.status_code, url))

    def get_page_number(self):
        if self.page_count > 0:
            return (self.page_count // 10) + 1
        else:
            return 1

    def add_link(self, link_html):
        url = link_html.get('href').replace('/url?q=', '')
        self.links.append(url)
        self.sites.pop(0)

    def get_links(self):
        for index in range(len(self.sites)):
            site = self.sites[0]
            print('{0} --> {1}'.format(index, site))

            while site in self.sites:
                link_html = self.get_page_html().find(href=re.compile(site))

                if link_html is None:
                    self.page_count += 10
                else:
                    print('We found "{0}" on page {1} of {2}'.format(site, self.get_page_number(), 'google.com'))
                    self.page_count = 0
                    self.add_link(link_html)
                    break

            print('--------------------------------')
        return self.links

    def run(self):
        links = self.get_links()
        print(links)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name to search google for...')
    args = parser.parse_args()

    try:
        print('Starting the Opt Out process...')
        obj = OptOut(args.name)
        obj.run()
    except Exception as err:
        print('Handling run-time error:', err)
    finally:
        print('Opt Out process has ended...')
