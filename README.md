By providing a url that contains a list of links to other pages by year (for example, the nav bar of a blog), this script takes the listed urls, navigates to them, parses their body text, and outputs the content as text files. 

It primarily uses selenium and beautiful soup together with python. I developed this as a side project while learning about automated web testing. There are more efficient ways of parsing and archiving data from the web.

Usage: python bscrape.py [optional flags] [URL]

Optional flags include:
-y: The earliest date to find from the web page
-h: Displays usage text (also displays upon unexpected formatting)
-n: the name of the file(s) to output. If it's not provided, it defaults to the page's domain name

The URL is required.

Work is still being done to sanitize the output, perhaps by recognizing where the actual content begins and ends, versus navigation, feeds, etc. Eventually, the goal is to move away from selenium and use a crawler for fetching links.

DISCLAIMER:
This is meant for educational purposes only. The ethical and legal issues regarding web crawlers would apply to this as well. Additionally, I hold no responsibility if you try to access a website too quickly and are blocked. Use at your own discretion.
