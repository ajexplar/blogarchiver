from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import requests

from datetime import datetime
import os
import re
import time

class Scraper:
    def __init__(self, logger):
        self.logger = logger
        self.first_url = None
        self.year = 2001
        self.basename = None

    def launch_driver(self):
        opts = Options()
        opts.add_argument('--headless')
        opts.binary_location = '/usr/bin/chromium'
        self.driver = webdriver.Chrome(chrome_options=opts)
        self.driver.wait = WebDriverWait(self.driver, 1)

    def close_driver(self):
        self.driver.quit()

    def provide_user_values(self, data):
        self.first_url = data['url']
        if 'start_date' in data:
            self.year = data['start_date']
        
        if 'file_name' in data:
            self.basename = data['file_name']
        else:
            self.basename = self.parse_url(self.first_url)

        self.logger.debug('Year:' + str(self.year))
        self.logger.debug('Base file name:' + self.basename)
        self.logger.debug('URL:' + self.first_url)

    def run(self):
        try:
            self.driver.get(self.first_url)
            urls_to_save = self.find_archives()
            logging.info('Urls found:' + str(urls_to_save))
            self.save_archives(urls_to_save)
        except Exception as e:
            logging.warn('EXCEPTION: ', e)
        finally:
            self.close_driver()

    def find_archives(self):
        xpath_pattern = '//a[contains(text(), %y) and contains(@href, "%s")]'  # %y is a placeholder for the year, %s is a placeholder to the current domain
        history_urls = []
        now = datetime.now()
        while self.year < now.year:
            xpath_on_page = xpath_pattern.replace('%y', str(self.year))
            xpath_on_page = xpath_on_page.replace('%s', self.basename)
            self.year += 1
            try:
                link_element = self.driver.find_element(By.XPATH, xpath_on_page)
                url = link_element.get_attribute('href')
                history_urls.append(url)
            except:
              continue 
        return history_urls

    def save_archives(self, url_list):
        cwd = os.getcwd()
        file_number = 1
        for url in url_list:
            time.sleep(5)
            html_doc = requests.get(url).content
            text = self.clean_source(html_doc)

            path_to_file = cwd + '/' + self.basename + '-' + str(file_number) + '.txt'
            file_number += 1

            with open(path_to_file, 'w+') as f:
                f.write(text)

            filename = path_to_file.split('/')
            logging.info('Created file ' + filename[-1])

    def parse_url(self, url):
        domainname = re.match('(?:(?:https?)://)?(?:www.)?([^/\r\n]+)(?:/[^\r\n]*)?', url)
        if domainname:
            if len(domainname.groups()) >= 1:
                domain = domainname.groups()[0]
                domain = domain.split('.')
                return domain[0]

    def clean_source(self, html):
        soup = BeautifulSoup(html, 'lxml') # a bit faster than the other implementations
        for script in soup(['script', 'style', 'meta', 'noscript']):
            script.extract()
        text = soup.get_text()
        return text

