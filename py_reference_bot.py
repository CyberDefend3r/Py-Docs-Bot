'''
Python Reference Bot for reddit.

This reddit bot will lurk the /r/learnpython subreddit and when invoked by keyword will reply with links to python documentation, online resources, and youtube videos for any python topic(s) requested. 

Creator: Trevor Miller
GitHub: https://github.com/trevormiller6
reddit: https://www.reddit.com/user/trevor_of_earth/

TODO:
 * Add flexability to syntax for seperation of command arguments (allow both comma space `, ` and just comma `,`)
 * Remove print() statements and set up actual logging
 * On a !py_howto search show the entire google query not just the search terms
 * Review and look for ways to optimize and possibily restructure/refactor code if needed
 * Move to heroku.com or something similar
'''

# Standard
import configparser
import re
import requests

# Non-standard
from googlesearch import search
from lxml.html import fromstring
import praw


def main():
    '''
    Main function
    '''

    print("Authenticating to reddit")
    # Instantiate reddit class and authenticate
    reddit = reddit_authenticate()
    # Define subreddit to monitor
    subreddit = reddit.subreddit(subreddit_name)
    print("Starting comments scanning")
    # Call function to start itterating through comments
    scan_comments(subreddit)

def reddit_authenticate():
    '''
    Authenticate to reddit
    '''

    reddit = praw.Reddit(client_id=reddit_api_id,
                         client_secret=reddit_api_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=bot_user_agent)

    return reddit

def scan_comments(subreddit):
    '''
    Loop through comments from the learnpython subreddit and check for bot keywords.
    If found parse the topics out and retrive related links to documentation and post a reply with the links gathered.
    '''

    # Loop over comment objects returned from reddit. skip_existing=True means that when the bot
    # starts it will not go back and get existing comments and instead start with new ones.
    for comment in subreddit.stream.comments(skip_existing=True):

        # Check for keyword !py_refs in comment. If found get reference links from python documentatiom, google, youtube.
        # Module paths are case sensitive.
        # command usage: !py_refs pathlib.path, re.search, requests
        if "!py\\_refs" in comment.body:
            try:
                needed_references = re.search(r"^\!py\\\_refs\s(.+)$", comment.body, flags=re.MULTILINE).group(1).split(", ")
                all_links = get_links(needed_references, "all")
                comment.reply(build_comment(all_links))
                print("replied to a comment")
            except AttributeError:
                continue

        # Check for keyword !py_official. If found get link to offical python documentation from https://docs.python.org/3/library/
        # Module paths are case sensitive.
        # Command usage: !py_official function.zip, function.enumerate, requests
        if "!py\\_official" in comment.body:
            try:
                needed_references = re.search(r"^\!py\\\_official\s(.+)$", comment.body, flags=re.MULTILINE).group(1).split(", ")
                all_links = get_links(needed_references, "official")
                comment.reply(build_comment(all_links))
                print("replied to a comment")
            except AttributeError:
                continue

        # Check for keyword !py_howto. If found get reference material from google and youtube. All that needs to be passed to the bot is the topic. The bot will
        # search google with the query: `how to <python topic> 'python'`
        # Command usage: !py_howto for loops, list comprehension
        if "!py\\_howto" in comment.body:
            try:
                needed_references = re.search(r"^\!py\\\_howto\s(.+)$", comment.body, flags=re.MULTILINE).group(1).split(", ")
                all_links = get_links(needed_references, "howto")
                comment.reply(build_comment(all_links))
                print("replied to a comment")
            except AttributeError:
                continue

def get_links(needed_references, reference_types):
    '''
    Gather all the links to reference materials requested.
    '''

    def _validate_and_markdown_format_link(link):
        '''
        Validate that the links gathered work and if they do format to markdown 
        with the actual page name else return an empty string.
        '''

        link_results = requests.get(link)

        if link_results:
            tree = fromstring(link_results.content)
            valid_link = f"[{tree.findtext('.//title')}]({link})"

            return valid_link

        else:

            return ""

    def _search_google(search_terms, search_type):
        '''
        get google and youtube reference links.
        Google query is structured `how to <search terms> 'python'`. Python is in quotes because that tells google
        that it must exist in the results that are returned. Safe search is on in case any user tries to get naughty.
        '''

        # Google video search specifically on the site youtube.com
        if search_type:
            google_links = search(f"site:youtube.com how to {search_terms} 'python'",
                                    tld="com",
                                    lang="english",
                                    country="us",
                                    safe="on",
                                    start=1,
                                    stop=3,
                                    extra_params={"tbm": search_type},
                                    user_agent=None)
            valid_google_links = [_validate_and_markdown_format_link(link) for link in google_links]

            return {"reference_vids": valid_google_links}

        # Regular google search
        else:
            google_links = search(f"how to {search_terms} 'python'",
                                    tld="com",
                                    lang="english",
                                    country="us",
                                    safe="on",
                                    start=1,
                                    stop=3,
                                    user_agent=None)
            valid_google_links = [_validate_and_markdown_format_link(link) for link in google_links]

            return {"reference_links": valid_google_links}
    
    def _get_official_docs(pymodule):
        '''
        Get link to official python documentation. Python kinda standardized their link structure for their documentation
        but there is a little weirdness that we check for.
        '''

        # For python built-in functions (zip, map, filter, enumerate, etc.), they did not get their own page and instead are all on one page.
        # I am requiring that the user puts `function.` infront of these function names to distiguish them from the other python libraries. 
        # Also, python has them all on a pgae called functions so I felt like it made sense
        # Split on the `.` and grab the second item in the list to build the link.
        if "function" in pymodule:
            link = f"https://docs.python.org/3/library/functions.html#{pymodule.split('.')[1]}"
            link_is_valid = _validate_and_markdown_format_link(link)

        # If function was not in the module name then attempt to create a link with the full module name, ex. `pathlib.Path`.
        # This serves 2 purposes: first to accomadate modules names that don't include class, and second for things like `os.path`
        # that for some reason has its own page in the docs seprate from the `os` docs.
        else:
            link = f"https://docs.python.org/3/library/{pymodule}.html#{pymodule}"
            link_is_valid = _validate_and_markdown_format_link(link)

        if link_is_valid:

            return {"official_links": link_is_valid}

        # If after testing the above links to python documentation fails than there is one last url path to try.
        # This is actually the url path that most of the documentation will have.
        # Split on the `.` and grab the first item in the list which will be the library name ex. pathlib.Path becomes just pathlib
        else:
            link = f"https://docs.python.org/3/library/{pymodule.split('.')[0]}.html#{pymodule}"
            link_is_valid = _validate_and_markdown_format_link(link)

            if link_is_valid:

                return {"official_links": link_is_valid}

            # If all of the above failed then it most likely is not a python standard library or function or the user had a typo.
            else:

                return {"official_links": " One of the following occured: This method is not part of the python standard library, you meant to do a `!py_howto` search or you misspelled the python module name. Module names are case sensitive ex. pathlib.Path note the capital `P` because that is how the actual class is called in python and the python doc creators used this in all the naming in their url's."}

    # Create the dictionary that will store all of our links using the python module name as the key.
    # In cases where !py_howto was used it will have the search terms.
    all_links = {pymodule: [] for pymodule in needed_references}
    
    # !py_refs was used so we are going to get links from all sources
    if reference_types == "all":

        for pymodule in needed_references:

            all_links[pymodule].append(_get_official_docs(pymodule))
            all_links[pymodule].append(_search_google(pymodule, None))
            all_links[pymodule].append(_search_google(pymodule, "vid"))

    # !py_official was used so we are only going to get a link to python docs
    if reference_types == "official":

        for pymodule in needed_references:

            all_links[pymodule].append(_get_official_docs(pymodule))

    # !py_howto was used so we are going to get links from google and youtube
    if reference_types == "howto":

        for pymodule in needed_references:

            all_links[pymodule].append(_search_google(pymodule, None))
            all_links[pymodule].append(_search_google(pymodule, "vid"))

    return all_links

def build_comment(all_links):
    '''
    Build the comment that will have all of the reference links.
    Format in markdown.
    '''

    comment_markdown = "**Thanks for using the Python Reference Bot!**\n*For available commands see [GitHub](https://github.com/trevormiller6/Py-Reference)*\n\n"
    new_line = "\n"

    for pymodule, link_list in all_links.items():

        module_links = f"# {pymodule}:\n"

        for link_type in link_list:

            if "official_links" in link_type:
                official_docs = f"\n\nOfficial Documentation:\n* {link_type['official_links']}"
                module_links += official_docs

            if "reference_links" in link_type:
                online_refs = f"\n\nOnline Resources:\n* {f'{new_line}* '.join(link_type['reference_links'])}"
                module_links += online_refs

            if "reference_vids" in link_type:
                online_vids = f"\n\nYoutube Videos:\n* {f'{new_line}* '.join(link_type['reference_vids'])}"
                module_links += online_vids

        comment_markdown += f"{module_links}\n\n"

    # If one of the links was not valid the validate function returns an empty string that when evaluated in this function
    # Gets formatted as `* \n` so I just strip that out before returning the comment.
    return comment_markdown.replace("* \n", "")


if __name__ == "__main__":
    print("reading in credentials")
    config = configparser.ConfigParser()
    config.read("credentials.ini")
    reddit_api_id = config["reddit"]["client_id"]
    reddit_api_secret = config["reddit"]["client_secret"]
    reddit_username = config["reddit"]["username"]
    reddit_password = config["reddit"]["password"]
    subreddit_name = "learnpython"
    bot_user_agent = "(praw-python3.9) py_reference_bot - scanning comments in /r/learnpython and replying with python references"

    while True:
        try:
            main()
        except Exception as e:
            print(e)
            continue
        except KeyboardInterrupt:
            print("Exiting")
            break
