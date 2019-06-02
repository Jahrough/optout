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

    @staticmethod
    def get_page_html(url):
        response = requests.get(url)
        if response.ok and response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            error_message = 'Status code {0} when trying to retrieve a response from "{1}"'
            raise Exception(error_message.format(response.status_code, url))

    def get_page_number(self):
        if self.page_count > 0:
            return (self.page_count // 10) + 1
        else:
            return 1

    def add_link(self, link_html):
        url = link_html.get('href').replace('/url?q=', '')
        self.links.append(url)
        self.sites.pop(0)

    def get_links_from_google(self):
        for index in range(len(self.sites)):
            site = self.sites[0]
            print('{0} --> {1}'.format(index, site))

            while site in self.sites:
                google_url = 'https://www.google.com/search?q={0}&start={1}'.format(self.name, self.page_count)
                link_html = OptOut.get_page_html(google_url).find(href=re.compile(site))

                if link_html is not None:
                    print('We found "{0}" on page {1} of {2}'.format(site, self.get_page_number(), 'google.com'))
                    self.page_count = 0
                    self.add_link(link_html)
                    break
                elif self.page_count > 100:
                    self.page_count = 0
                    self.sites.pop(0)
                    print('you have reached the limit for searching for', site)
                    break
                else:
                    self.page_count += 10

            print('\n--------------------------------\n')
        return self.links

    def run(self):
        links = self.get_links_from_google()
        print(links)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name to search google for...')
    args = parser.parse_args()

    try:
        print('\n <<< Starting the Opt Out process... >>> \n')
        obj = OptOut(args.name)
        obj.run()
    except Exception as err:
        print('Handling run-time error:', err)
    finally:
        print('\n <<< Opt Out process has ended... >>> \n')
