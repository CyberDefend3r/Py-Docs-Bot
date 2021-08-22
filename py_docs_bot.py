'''
Python Documentation Bot for reddit.

This reddit bot will monitor the /r/learnpython subreddit and when invoked by keyword will reply with links to python documentation for any python topic(s) requested. 

Creator: Trevor Miller
GitHub: https://github.com/trevormiller6
reddit: https://www.reddit.com/user/trevor_of_earth/
Bot's reddit: https://www.reddit.com/user/py_reference_bot
'''

import configparser
from json import loads
import logging
from os import environ
import re
import requests
from fuzzywuzzy import fuzz
import praw


def main():
    '''
    Main function to initalize reddit class and authenticate
    '''

    # Try to get bot credentials from the file 'credentials.ini' located in script directory
    try:
        config = configparser.ConfigParser()
        config.read("credentials.ini")
        reddit_api_id = config["reddit"]["client_id"]
        reddit_api_secret = config["reddit"]["client_secret"]
        reddit_username = config["reddit"]["username"]
        reddit_password = config["reddit"]["password"]
    except Exception:
        logger.error("No credentials.ini file found. Checking environment variables.")
        # Failed to get creds from file so lets check the environment variables.
        try:
            reddit_api_id = environ["REDDIT_DOC_BOT_ID"]
            reddit_api_secret = environ["REDDIT_DOC_BOT_SECRET"]
            reddit_username = environ["REDDIT_DOC_BOT_USER"]
            reddit_password = environ["REDDIT_DOC_BOT_PASSWORD"]
        except KeyError:
            logger.critical("environment variables not found")
            raise SystemExit

    bot_user_agent = "(praw-python3.9) py_docs_bot - scanning comments in /r/learnpython and replying with python documentation links"
    logger.info("Authenticating to reddit")
    # Instantiate reddit class and authenticate
    reddit = praw.Reddit(client_id=reddit_api_id,
                         client_secret=reddit_api_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=bot_user_agent)
    logger.info("Authentication successfull to redit.com")
    # Define subreddit to monitor
    subreddit = reddit.subreddit("learnpython")
    # Call function to start itterating through comments
    monitor_and_reply_to_comments(subreddit)

def monitor_and_reply_to_comments(subreddit):
    '''
    Loop through comments from the learnpython subreddit and check for bot keyword.
    If found parse the topics out and retrive related links to documentation and post a reply with the links.
    '''

    logger.info("Monitoring r/learnpython comments for keyword '!docs'")

    # Loop over comment objects returned from reddit. skip_existing=True means that when the bot
    # starts it will not go back and get existing comments and instead start with new ones.
    for comment in subreddit.stream.comments(skip_existing=True):

        # Check for keyword !docs in comment. If found get reference links from python documentatiom
        # Module paths are case sensitive.
        # command usage: !docs pathlib.Path, re.search, requests, zip
        if bool(re.search(r"^\!docs.+$", comment.body, flags=re.MULTILINE)):
            logger.info("New command recieved: %s", comment.body)
            needed_references = re.search(r"^\!docs\s(.+)$", comment.body, flags=re.MULTILINE).group(1).replace(" ", "").split(",")
            all_links = _get_links(needed_references)

            if all_links:
                bot_reply = _build_comment(all_links)
                comment.reply(bot_reply)
                logger.info("Replied to a comment: %s", bot_reply)

def _get_links(needed_references):
    '''
    Gather all the links to reference materials requested.
    '''

    # Create the dictionary that will store all of our links using the python module or search terms as the key.
    all_links = {}

    for reference in needed_references:

        ref_links = [link for link in _get_official_docs(reference) if link]

        if ref_links:
            all_links[reference] = ref_links

    return all_links

def _get_official_docs(reference):
    '''
    Get link to official python documentation. 
    '''

    def _standard_library():
        '''
        Get links to the documentation on the standard library. 
        Python kinda standardized their link structure for their documentation 
        but there is a little weirdness that we check for.
        '''

        def _is_link_valid():
            '''
            Validate that the links gathered work and if they do format to markdown 
            with the actual page name else return an empty string.
            '''

            link_results = requests.get(link)

            if link_results:

                return True

            else:

                return False

        builtin_functions = ["abs", "delattr", "hash", "memoryview", "set", "all", "dict", "help", "min", "setattr", "any", "dir", "hex", "next", "slice", "ascii", 
                            "divmod", "id", "object", "sorted", "bin", "enumerate", "input", "oct", "staticmethod", "bool", "eval", "int", "open", "str", "breakpoint", 
                            "exec", "isinstance", "ord", "sum", "bytearray", "filter", "issubclass", "pow", "super", "bytes", "float", "iter", "print", "tuple", "callable", 
                            "format", "len", "property", "type", "chr", "frozenset", "list", "range", "vars", "classmethod", "getattr", "locals", "repr", "zip", "compile", 
                            "globals", "map", "reversed", "__import__", "complex", "hasattr", "max", "round"]

        # For python built-in functions (zip, map, filter, enumerate, etc.), they did not get their own page and instead are all on one page.
        if reference in builtin_functions:
            link = f"https://docs.python.org/3/library/functions.html#{reference}"
        # If function was not in the module name then attempt to create a link with the full module name, ex. `pathlib.Path`.
        # This serves 2 purposes: first to accomadate modules names that don't include class, and second for things like `os.path`
        # that for some reason has its own page in the docs seprate from the `os` docs.
        else:
            link = f"https://docs.python.org/3/library/{reference}.html#{reference}"

        if _is_link_valid():

            return f"[{reference} - {link}]({link})  \n"

        # If after testing the above links to python documentation fails than there is one last url path to try.
        # This is actually the url path that most of the documentation will have.
        # Split on the `.` and grab the first item in the list which will be the library name ex. pathlib.Path becomes just pathlib
        else:
            link = f"https://docs.python.org/3/library/{reference.split('.')[0]}.html#{reference}"

            if _is_link_valid():

                return f"[{reference} - {link}]({link})  \n"

            # If all of the above failed then it most likely is not a python standard library or function or the user had a typo.
            else:

                return False

    def _reference_docs():
        '''
        Get links to reference documentation from the python docs site.
        I use fuzzy searching here so that docs called up without having to know the actual title of the reference
        that is being requested. Requires a minimum match score of 85. May need to tweak this number... not sure yet.
        '''

        matched_references = []

        for link_dict in REFLINKS["python_ref_docs_url_data"]:

            match_ratio = fuzz.token_set_ratio(link_dict["title"], reference)

            if match_ratio > 85:
                matched_references.append(f'[{link_dict["title"]} - {REFLINKS["python_ref_docs_base_url"]}{link_dict["link"]}]({REFLINKS["python_ref_docs_base_url"]}{link_dict["link"]})  \n')

        if matched_references:

            return matched_references

        else:

            return []

    combined_links = [_standard_library(), *_reference_docs()]
    
    return combined_links
    

def _build_comment(all_links):
    '''
    Build the comment that will have all of the reference links.
    Format in markdown.
    '''

    comment_markdown = ""

    for links in all_links.values():
        if isinstance(links, list):
            for link in links:
                comment_markdown += link
        else:
            comment_markdown += link

    comment_markdown += f"  \nPython Documentation Bot - *[How To Use](https://github.com/trevormiller6/Py-Docs-Bot)*"

    return comment_markdown


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger=logging.getLogger("py_docs_bot")
    
    with open("python_reference_docs.json", "r") as file:
        REFLINKS = loads(file.read())

    while True:
        try:
            logger.info("Starting up...")
            main()
        except Exception as e:
            logger.error(e)
            continue
        except (KeyboardInterrupt, SystemExit):
            logging.error("Exiting due to no credentials or keyboard interrupt.")
            raise SystemExit
