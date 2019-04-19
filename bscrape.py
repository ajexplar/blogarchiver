import logging
import sys

from scraper import Scraper

def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    data = parse_arguments(sys.argv)

    if len(data) >= 1:
        scour = Scraper(logger)
        scour.provide_user_values(data)
        scour.launch_webdriver()
        scour.run()

def parse_arguments(args):
    help_text = '''USE: bscrape.py [arguments]  http(s)://[url]\n
        Arguments are optional. You can use:\n
        \t-y: Earliest date to find
        \t-h: This usage text
        \t-n: Use your own name for the outputted files
        The url is required. It ought to be a page that contains a list of page's in the site's history
    ''' 
    user_args = args[1:]
    if len(user_args) == 0:
        logging.info(help_text)
        return {}
    else:
        user_data = {}
        dirty_flag = False
        logging.debug('User Args:' + str(user_args))
        args_iter = iter(range(len(user_args)))
        for i in args_iter:
            if user_args[i] == '-h':
                logging.info(help_text)
                return {}
            else:
                if user_args[i] == '-y':
                    if i+1 < len(user_args):
                        user_data['start_date'] = user_args[i+1]
                        next(args_iter)
                    else:
                        dirty_flag = True
                        break
                elif user_args[i] == '-n':
                    if i+1 < len(user_args):
                        user_data['file_name'] = user_args[i+1]
                        next(args_iter)
                    else:
                        dirty_flag = True
                        break
                else:
                    user_data['url'] = user_args[i]
                    break

        if dirty_flag:
            logging.debug('Argument flag is missing a value')
            logging.info(help_text)
            return {}
        else:
            return user_data

if __name__ == '__main__':
    main()
