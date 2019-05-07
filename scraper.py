import logging
import os
import re
import time

#from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

class ScraperX():
    def __init__(self):
        logging.debug('Initialized Scraper')
        self.site = None
        self.path = None
        self.bodytext = False
        self.verbose = False
        self.depth = 0
        self.filename = None
        self.driver = None
        self.number = 1

        self.launch_driver()

    def launch_driver(self):
        logging.debug('Launching webdriver')
        opts = Options()
        opts.add_argument('--headless')
        opts.binary_location = '/usr/bin/chromium'
        self.driver = webdriver.Chrome(chrome_options=opts)
        self.driver.wait = WebDriverWait(self.driver, 3)

    def closedown_driver(self):
        self.driver.quit()

    def assign_vars(self, args):
        logging.debug('Assigning variables')

        self.first_url = args['url']
        self.path = args['path']

        if not os.path.isdir(self.path):
            logging.warn('Path must be a valid directory')
            return False
        else:
            if not self.path.endswith('/'):
                self.path = self.path + '/'

        self.bodytext = True if args['bodytext'] is not None else False
        self.verbose = True if args['verbose'] is not None else False

        if args['depth'] is not None:
            if args['depth'] < 0:
                logging.warn('Depth must be greater or equal to 0')
                return False
            self.depth = args['depth']

        if args['filename'] is not None:
            self.filename = args['filename']
        else:
            self.filename = self.extract_domain(self.first_url)

        logging.debug('\nURL: {}\nPath: {}\nBody Only: {}\nVerbose: {}\nDepth: {}\nFilename: {}\n'.format(self.first_url, self.path, self.bodytext, self.verbose, self.depth, self.filename))
        return True

    def extract_domain(self, url):
        logging.debug('Extract domain from url')
        matched = re.match('(?:(?:https?)://)?(?:www.)?([^/\r\n]+)(?:/[^\r\n]*)?', url)
        if matched:
            if len(matched.groups()) >= 1:
                domain = matched.groups()[0]
                domain = domain.split('.')
                if self.verbose:
                    logging.info('Using {} as the base filename'.format(domain[0]))
                return domain[0]
        else:
            return None

    def scrape(self):
        if self.verbose:
            logging.info('Scraping started')

        try:
            depth = 0
            urls = [[self.first_url]]
            archived = [self.first_url]
            while len(urls) > 0 and depth <= self.depth:
                to_add = []
                for u in urls[0]:
                    self.parse_data(u)
                    found_urls = self.find_urls(u, archived)
                    to_add.extend(found_urls)
                urls.pop(0)
                urls.append(to_add)
                archived.extend(to_add)
                if self.verbose:
                    logging.info('Depth={}'.format(depth))
                logging.debug(urls)
                # pprint(urls)
                # pprint(archived)
                depth += 1
        except Exception as e:
            logging.warn('EXCEPTION: {}'.format(e))
        finally:
            self.closedown_driver()

    def parse_data(self, url):
        full_path = self.path + self.filename + '-' + str(self.number)
        if self.bodytext:
            html_doc = self.clean_source(self.driver.page_source)
        else:
            html_doc = self.driver.page_source

        with open(full_path, 'w+') as f:
            if self.verbose:
                logging.info('Writing to {}'.format(full_path))
            f.write(html_doc)
        self.number += 1

    def clean_source(self, page):
        soup = BeautifulSoup(page, 'lxml') # lxml is a bit faster than other implementations
        for script in soup(['script', 'style', 'meta', 'head', 'title', 'noscript']):
            script.extract()
        text = soup.get_text()
        clean_text = re.sub('\n+', '\n', text).strip()
        return clean_text

    def find_urls(self, url, archived):
        linked_pages = []
        if not url.startswith('http'):
            url = 'http://' + url
        self.driver.get(url)
        time.sleep(3)
        
        if self.verbose:
            logging.info('Finding links from {}'.format(url))

        all_links = self.driver.find_elements(By.TAG_NAME, 'a')
        for link in all_links:
            link_value = link.get_attribute('href')
            if '#' in link_value:  # skip internal page links
                continue
            if self.first_url not in link_value: # skip external links
                continue
            if link_value not in archived and link_value not in linked_pages:
                linked_pages.append(link_value)
        return linked_pages

