"""
Python Documentation Bot for reddit.

This reddit bot will monitor the /r/learnpython subreddit and when invoked by keyword
will reply with links to python documentation for any python topic(s) requested.

Creator: Trevor Miller
GitHub: https://github.com/trevormiller6
reddit: https://www.reddit.com/user/trevor_of_earth/
Bot's reddit: https://www.reddit.com/user/py_reference_bot
"""


import configparser
from json import loads
import logging
from os import environ
from pathlib import Path
import re
import requests
from fuzzywuzzy import fuzz
import praw
import google.cloud.logging


# Setup logging
client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )
# LOGGER = logging.getLogger("py_docs_bot")


# Making this variable a global so that it doesnt open and close the file
# everytime it needs the data in the functions that require it
try:
    datastore_path = Path.cwd() / "datastore" / "datastore.json"
    with open(datastore_path, "r") as datastore_file:
        DATASTORE = loads(datastore_file.read())
    logging.info("Set global variable 'DATASTORE' from file: datastore.json.")
except Exception as e:
    logging.error("Could not open file 'datastore.json'. %s", e)
    raise SystemExit


def monitor_and_reply_to_comments(subreddit):
    """
    Loop through comments from the learnpython subreddit and check for bot keyword.
    If found parse the topics out and retrive related links to documentation and post a reply with the links.
    """

    logging.info("Monitoring r/learnpython comments for keyword '!docs'")

    # Loop over comment objects returned from reddit. skip_existing=True means that when the bot
    # starts it will not go back and get existing comments and instead start with new ones.
    for comment in subreddit.stream.comments(skip_existing=True):
        logging.info(comment.body)

        # Check for keyword !docs in comment. If found get reference links from python documentatiom
        # Module paths are case sensitive.
        # Command usage: !docs pathlib.Path, re.search, zip, while
        if bool(re.search(r"^\!docs.+$", comment.body, flags=re.MULTILINE)):
            logging.info("New command recieved: %s", repr(comment.body))
            needed_references = (
                re.search(r"^\!docs\s(.+)$", comment.body, flags=re.MULTILINE)
                .group(1)
                .replace(" ", "")
                .split(",")
            )

            # Filter out empty strings for queries that returned no results
            all_links = [
                link for link in _get_links_to_python_docs(needed_references) if link
            ]

            if all_links:
                comment_markdown = f"{''.join(all_links)}  \nPython Documentation Bot - *[How To Use](https://github.com/trevormiller6/Py-Docs-Bot)*"
                comment.reply(comment_markdown)
                logging.info("Replied to a comment: %s", repr(comment_markdown))
            else:
                logging.error(
                    "The request was not valid no response sent. Requested docs: %s",
                    needed_references,
                )


def _get_links_to_python_docs(needed_references):
    """
    Get link to official python documentation.
    """

    def _python_enhancement_proposals(reference):
        """
        Get links to python peps
        """

        reference = reference.lower()

        # Python easter egg
        # Just for fun
        if reference in ["zen", "zenofpython", "pep-20"]:

            return "[The Zen of Python:](https://www.python.org/dev/peps/pep-0020)  \n    import this\n  \n"

        # Extract the pep number
        try:
            _, pep_number = reference.split("-")
        except Exception:  # pylint:disable=broad-except
            return ""

        #  Make sure it is actually a number
        try:
            pep_number = int(pep_number)
            pep_number = str(pep_number)
        except ValueError:
            return ""

        # Pep numbers have 4 numbers in the url
        while len(pep_number) < 4:
            pep_number = f"0{pep_number}"

        link = f"https://www.python.org/dev/peps/pep-{pep_number}"

        return (
            f"[{reference.upper()} - {link}]({link})  \n"
            if bool(requests.get(link))
            else ""
        )

    def _language_reference_docs(reference):
        """
        Get links to reference documentation from the python docs site.
        I use fuzzy searching here so that docs called up without having to know the actual title of the reference
        that is being requested. Requires a minimum match score of 85. May need to tweak this number... not sure yet.
        """

        matched_references = []

        for reference_entry in DATASTORE["docs_sections"]:

            match_ratio = fuzz.token_set_ratio(
                reference_entry["title"], reference.lower()
            )

            if match_ratio > 85:
                matched_references.append(
                    f'[{reference_entry["title"].title()} - {reference_entry["link"]}]({reference_entry["link"]})  \n'
                )

        return "".join(matched_references) if matched_references else ""

    def _library_reference_docs(reference):
        """
        Get links to the documentation on the standard library.
        Python kinda standardized their link structure for their documentation
        but there is a little weirdness that we check for.
        """

        # For python built-in functions (zip, map, filter, enumerate, etc.), they did not get their own
        # page and instead are all on one page.
        # So the only thing we needed to set was the page anchor
        if reference in DATASTORE["builtin_functions"]:
            link = f"https://docs.python.org/3/library/functions.html#{reference}"
        # If the reference was not a built-in function attempt to create a link with the full module name,
        # ex. `pathlib.Path`.
        # This serves 2 purposes: first to accomadate modules names that don't include class, and second
        # for things like `os.path` that for some reason has its own page in the docs seprate from the `os` docs.
        else:
            link = f"https://docs.python.org/3/library/{reference}.html#{reference}"

        if bool(requests.get(link)):

            return f"[{reference} - {link}]({link})  \n"

        # If after testing the above links to python documentation fails than there is one last url path to try.
        # This is actually the url path that most of the documentation will have.
        # Split on the `.` and grab the first item in the list which will be the library name ex. pathlib.Path
        # becomes just pathlib which will be the name of the html file we want to go to. Then we use the full
        # method path `pathlib.Path` for the page anchor
        else:
            link = f"https://docs.python.org/3/library/{reference.split('.')[0]}.html#{reference}"

            return (
                f"[{reference} - {link}]({link})  \n"
                if bool(requests.get(link))
                else ""
            )

            # If all of the above failed then it most likely is not a python standard library or function
            # or the user had a typo.

    # Loop over each term that was requested by user and get the docs link
    all_links = [
        _library_reference_docs(reference)
        + _language_reference_docs(reference)
        + _python_enhancement_proposals(reference)
        for reference in needed_references
    ]

    return all_links


def main():
    """
    Main function to initalize reddit class and authenticate
    """

    # Try to get bot credentials from the file 'credentials.ini' located in script directory
    try:
        config = configparser.ConfigParser()
        config.read("credentials.ini")
        reddit_api_id = config["reddit"]["client_id"]
        reddit_api_secret = config["reddit"]["client_secret"]
        reddit_username = config["reddit"]["username"]
        reddit_password = config["reddit"]["password"]
    except Exception:  # pylint:disable=broad-except
        logging.error("No credentials.ini file found. Checking environment variables.")
        # Failed to get creds from file so lets check the environment variables.
        try:
            reddit_api_id = environ["REDDIT_DOC_BOT_ID"]
            reddit_api_secret = environ["REDDIT_DOC_BOT_SECRET"]
            reddit_username = environ["REDDIT_DOC_BOT_USER"]
            reddit_password = environ["REDDIT_DOC_BOT_PASSWORD"]
        except KeyError:
            logging.critical("environment variables not found")
            raise SystemExit

    bot_user_agent = "(praw-python3.9) py_docs_bot - scanning comments in /r/learnpython and replying with python documentation links"
    logging.info("Authenticating to reddit")
    # Instantiate reddit class and authenticate
    reddit = praw.Reddit(
        client_id=reddit_api_id,
        client_secret=reddit_api_secret,
        username=reddit_username,
        password=reddit_password,
        user_agent=bot_user_agent,
    )
    logging.info("Authentication successfull to redit.com")
    # Define subreddit to monitor
    subreddit = reddit.subreddit("learnpython")
    # Call function to start itterating through comments
    monitor_and_reply_to_comments(subreddit)


if __name__ == "__main__":

    while True:
        try:
            logging.info("Python Documentation Bot is Starting Up.")
            main()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Good Bye!")
            raise SystemExit
        except Exception as e:  # pylint:disable=broad-except
            logging.error("Something happened. Starting over! Error: %s", e)
            continue
