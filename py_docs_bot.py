'''
Python Documentation Bot for reddit.

This reddit bot will monitor the /r/learnpython subreddit and when invoked by keyword will reply with links to python documentation for any python topic(s) requested. 

Creator: Trevor Miller
GitHub: https://github.com/trevormiller6
reddit: https://www.reddit.com/user/trevor_of_earth/
Bot's reddit: https://www.reddit.com/user/py_reference_bot

TODO:
 * Remove print() statements and set up actual logging
 * Move to heroku.com or something similar if becomes popular... likely wont be needed...
'''

import configparser
from os import environ
import re
import requests
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
        print("No credentials.ini file found")
        # Failed to get creds from file so lets check the environment variables.
        try:
            reddit_api_id = environ["REDDIT_DOC_BOT_ID"]
            reddit_api_secret = environ["REDDIT_DOC_BOT_SECRET"]
            reddit_username = environ["REDDIT_DOC_BOT_USER"]
            reddit_password = environ["REDDIT_DOC_BOT_PASSWORD"]
        except KeyError:
            print("environment variables not found")
            raise SystemExit

    bot_user_agent = "(praw-python3.9) py_docs_bot - scanning comments in /r/learnpython and replying with python documentation links"
    print("Authenticating to reddit")
    # Instantiate reddit class and authenticate
    reddit = praw.Reddit(client_id=reddit_api_id,
                         client_secret=reddit_api_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=bot_user_agent)
    # Define subreddit to monitor
    subreddit = reddit.subreddit("learnpython")
    # Call function to start itterating through comments
    monitor_and_reply_to_comments(subreddit)

def monitor_and_reply_to_comments(subreddit):
    '''
    Loop through comments from the learnpython subreddit and check for bot keyword.
    If found parse the topics out and retrive related links to documentation and post a reply with the links.
    '''

    print("Monitoring r/learnpython comments for keyword '!docs'")

    # Loop over comment objects returned from reddit. skip_existing=True means that when the bot
    # starts it will not go back and get existing comments and instead start with new ones.
    for comment in subreddit.stream.comments(skip_existing=True):

        # Check for keyword !docs in comment. If found get reference links from python documentatiom
        # Module paths are case sensitive.
        # command usage: !docs pathlib.Path, re.search, requests, zip
        if bool(re.search(r"^\!docs.+$", comment.body, flags=re.MULTILINE)):
            needed_references = re.search(r"^\!docs\s(.+)$", comment.body, flags=re.MULTILINE).group(1).replace(" ", "").split(",")
            all_links = _get_links(needed_references)

            if all_links:
                comment.reply(_build_comment(all_links))
                print("replied to a comment")

def _get_links(needed_references):
    '''
    Gather all the links to reference materials requested.
    '''

    # Create the dictionary that will store all of our links using the python module or search terms as the key.
    all_links = {}

    for reference in needed_references:

        ref_link =_get_official_docs(reference)

        if ref_link:
            all_links[reference] = ref_link

    return all_links

def _get_official_docs(reference):
    '''
    Get link to official python documentation. Python kinda standardized their link structure for their documentation
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

        return link

    # If after testing the above links to python documentation fails than there is one last url path to try.
    # This is actually the url path that most of the documentation will have.
    # Split on the `.` and grab the first item in the list which will be the library name ex. pathlib.Path becomes just pathlib
    else:
        link = f"https://docs.python.org/3/library/{reference.split('.')[0]}.html#{reference}"

        if _is_link_valid():

            return link

        # If all of the above failed then it most likely is not a python standard library or function or the user had a typo.
        else:

            return False

def _build_comment(all_links):
    '''
    Build the comment that will have all of the reference links.
    Format in markdown.
    '''

    new_line = "  \n"
    comment_markdown = f"Python Docs:{new_line}"

    for reference, link in all_links.items():
        comment_markdown += f"[{reference} - {link}]({link}){new_line}"

    comment_markdown += f"{new_line}Python Documentation Bot - *[GitHub](https://github.com/trevormiller6/Py-Docs-Bot)*"

    return comment_markdown

if __name__ == "__main__":

    while True:
        try:
            main()
        except Exception as e:
            print(e)
            continue
        except (KeyboardInterrupt, SystemExit):
            print("Exiting")
            raise SystemExit
