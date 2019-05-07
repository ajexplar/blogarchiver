import argparse
import logging

from scraper import ScraperX

def argprep():
    logging.debug('Collecting arguments')
    parser = argparse.ArgumentParser()

    parser.add_argument('url', help='The url of the website to begin scraping from')
    parser.add_argument('path', help='The path to save scraped files to')

    parser.add_argument('-d', '--depth', help='How many links deep the scraper should go from the first page (defaults to only one page)', type=int)
    parser.add_argument('-b', '--bodytext', help='Attempts to extract the text within the body of the page only', action='store_true')
    parser.add_argument('-f', '--filename', help='The filename to save the scraped info to. Defaults to the webhost\'s name')
    parser.add_argument('-v', '--verbose', help='Shows information on each step of the scraping-saving process', action='store_true')

    args = parser.parse_args()
    return vars(args)

def main():
    logging.basicConfig(level=logging.INFO)
    logging.debug('Started logging')

    args = argprep()

    scraper = ScraperX()
    if scraper.assign_vars(args): # only proceed if arguments were passed in OK
        scraper.scrape()

if __name__ == '__main__':
    main()
