## Page Archiver

Given a root or home page, this Python 3 script takes all the links that are in the same domain and begins parsing them one-by-one in a depth-first manner, saving the body to the directory specified by the user.

## How it works
The script uses the Beautiful Soup library to handle page data, Selenium to find links on the page and navigating to them, and everything else is done with plain old Python. In particular, argparser handles the heavy duty work with user-provided arguments. 

I developed this as a side project while learning about automated web testing. There are faster ways to parse web data. Ideally, one would use a proper web crawler or official API for this task, but this works well enough for most web pages.

### Usage

From the --help flag:

```
usage: bscrape.py [-h] [-d DEPTH] [-b] [-f FILENAME] [-v] url path

positional arguments:
  url                   The url of the website to begin scraping from
  path                  The path to save scraped files to

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        How many links deep the scraper should go from the
                        first page (defaults to only one page)
  -b, --bodytext        If possible, extract the text within the body of the
                        page only
  -f FILENAME, --filename FILENAME
                        The filename to save the scraped info to. Defaults to
                        the webhost's name
  -v, --verbose         Shows information on each step of the scraping-saving
                        process
```

You will note that the url and path are required.

## TODO
* Validate URL (as opposed to failing when Selenium can't access it)
* Use more exact parsing
* Give the user a timeout flag in seconds (but set a minimum that can override attempts to be too quick)
* Give the user a year flag to only get pages newer than a certain time
* Recognize media, like images and files, and try to download them separately
* Include CSS styling when downloading the entire html page

## DISCLAIMER
The netiquette, not to mention legal issues, regarding web crawlers would apply to this project as well. This is meant for educational purposes only. Please do not use this on sites that do not allow bots. Furthermore, there is a default cooldown so the script pauses between requests, but I hold no responsibility if you try to access a website too quickly and are blocked. You use this script at your own discretion.
