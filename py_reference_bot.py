'''
Python Reference Bot for reddit.

This reddit bot will monitor the /r/learnpython subreddit and when invoked by keyword will reply with links to python documentation for any python topic(s) requested. 

Creator: Trevor Miller
GitHub: https://github.com/trevormiller6
reddit: https://www.reddit.com/user/trevor_of_earth/

TODO:
 * Handle rate limiting imposed by reddit
 * Remove print() statements and set up actual logging
 * Review for ways to optimize and possibily restructure/refactor code if needed
 * Move to heroku.com or something similar
'''

# Standard
import configparser
import re
import requests
#from time import sleep

# Non-standard
#from googlesearch import search
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
    monitor_comments(subreddit)

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

def monitor_comments(subreddit):
    '''
    Loop through comments from the learnpython subreddit and check for bot keyword.
    If found parse the topics out and retrive related links to documentation and post a reply with the links.
    '''

    # Loop over comment objects returned from reddit. skip_existing=True means that when the bot
    # starts it will not go back and get existing comments and instead start with new ones.
    for comment in ["!docs sys.path"]:#subreddit.stream.comments(skip_existing=True):

        # Check for keyword !docs in comment. If found get reference links from python documentatiom
        # Module paths are case sensitive.
        # command usage: !docs pathlib.Path, re.search, requests
        if bool(re.search(r"^\!docs\s(.+)$", comment, flags=re.MULTILINE)):

            needed_references = re.search(r"^\!docs\s(.+)$", comment, flags=re.MULTILINE).group(1)
            
            if bool(re.search(r"\s\,\s", needed_references)):
                needed_references = needed_references.split(" , ")
            elif bool(re.search(r"\,\s", needed_references)):
                needed_references = needed_references.split(", ")
            else:
                needed_references = needed_references.split(",")

            all_links = get_links(needed_references)
            with open("response.md", "w", encoding="utf-8") as file:
                file.write(build_comment(all_links))
            #comment.reply(build_comment(all_links))
            print("replied to a comment")

def get_links(needed_references):
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

    # def _search_google(search_terms, search_type):
    #     '''
    #     get google and youtube reference links.
    #     Google query is structured `how to <search terms> 'python'`. Python is in quotes because that tells google
    #     that it must exist in the results that are returned. Safe search is on in case any user tries to get naughty.
    #     '''

    #     # Google video search specifically on the site youtube.com
    #     if search_type:
    #         google_links = search(f"site:youtube.com how to {search_terms} 'python'",
    #                                 tld="com",
    #                                 lang="english",
    #                                 country="us",
    #                                 safe="on",
    #                                 start=1,
    #                                 stop=3,
    #                                 extra_params={"tbm": search_type},
    #                                 user_agent=None)
    #         valid_google_links = [_validate_and_markdown_format_link(link) for link in google_links]

    #         return {"reference_vids": valid_google_links}

    #     # Regular google search
    #     else:
    #         google_links = search(f"how to {search_terms} 'python'",
    #                                 tld="com",
    #                                 lang="english",
    #                                 country="us",
    #                                 safe="on",
    #                                 start=1,
    #                                 stop=3,
    #                                 user_agent=None)
    #         valid_google_links = [_validate_and_markdown_format_link(link) for link in google_links]

    #         return {"reference_links": valid_google_links}
    
    def _get_official_docs(reference):
        '''
        Get link to official python documentation. Python kinda standardized their link structure for their documentation
        but there is a little weirdness that we check for.
        '''

        builtin_functions = ["abs", "delattr", "hash", "memoryview", "set", "all", "dict", "help", "min", "setattr", "any", "dir", "hex", "next", "slice", "ascii", 
                            "divmod", "id", "object", "sorted", "bin", "enumerate", "input", "oct", "staticmethod", "bool", "eval", "int", "open", "str", "breakpoint", 
                            "exec", "isinstance", "ord", "sum", "bytearray", "filter", "issubclass", "pow", "super", "bytes", "float", "iter", "print", "tuple", "callable", 
                            "format", "len", "property", "type", "chr", "frozenset", "list", "range", "vars", "classmethod", "getattr", "locals", "repr", "zip", "compile", 
                            "globals", "map", "reversed", "__import__", "complex", "hasattr", "max", "round"]

        # For python built-in functions (zip, map, filter, enumerate, etc.), they did not get their own page and instead are all on one page.
        if reference in builtin_functions:
            link = f"https://docs.python.org/3/library/functions.html#{reference}"
            link_is_valid = _validate_and_markdown_format_link(link)

        # If function was not in the module name then attempt to create a link with the full module name, ex. `pathlib.Path`.
        # This serves 2 purposes: first to accomadate modules names that don't include class, and second for things like `os.path`
        # that for some reason has its own page in the docs seprate from the `os` docs.
        else:
            link = f"https://docs.python.org/3/library/{reference}.html#{reference}"
            link_is_valid = _validate_and_markdown_format_link(link)

        if link_is_valid:

            return {"official_links": link_is_valid}

        # If after testing the above links to python documentation fails than there is one last url path to try.
        # This is actually the url path that most of the documentation will have.
        # Split on the `.` and grab the first item in the list which will be the library name ex. pathlib.Path becomes just pathlib
        else:
            link = f"https://docs.python.org/3/library/{reference.split('.')[0]}.html#{reference}"
            link_is_valid = _validate_and_markdown_format_link(link)

            if link_is_valid:

                return {"official_links": link_is_valid}

            # If all of the above failed then it most likely is not a python standard library or function or the user had a typo.
            else:

                return {"": ""}

    # Create the dictionary that will store all of our links using the python module or search terms as the key.
    all_links = {reference: [] for reference in needed_references}
    
    for reference in needed_references:

        all_links[reference].append(_get_official_docs(reference))

        # if " " in reference:
        #     all_links[reference].append(_search_google(reference, None))
        #     all_links[reference].append(_search_google(reference, "vid"))
        # else:
        #     all_links[reference].append(_get_official_docs(reference))
        #     all_links[reference].append(_search_google(reference, None))
        #     all_links[reference].append(_search_google(reference, "vid"))

    return all_links

def build_comment(all_links):
    '''
    Build the comment that will have all of the reference links.
    Format in markdown.
    '''

    comment_markdown = ""
    # new_line = "\n"

    for reference, link_list in all_links.items():

        module_links = f"Docs for {reference}:  \n"

        for link_type in link_list:

            if "official_links" in link_type:
                official_docs = f"{link_type['official_links']}  "
                module_links += official_docs

            # if "reference_links" in link_type:
            #     online_refs = f"\n\nOnline Resources:  \n- {f'  {new_line}- '.join(link_type['reference_links'])}"
            #     module_links += online_refs

            # if "reference_vids" in link_type:
            #     online_vids = f"\n\nYoutube Videos:  \n- {f'  {new_line}- '.join(link_type['reference_vids'])}"
            #     module_links += online_vids

        comment_markdown += f"{module_links}  \n"
    comment_markdown += "  \nPython Reference Bot - *Documentation on [GitHub](https://github.com/trevormiller6/Py-Reference)*"
    # If one of the links was not valid the validate function returns an empty string that when evaluated in this function
    # Gets formatted as `- \n` so I just strip that out before returning the comment.
    return comment_markdown.replace("- \n", "")


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
    main()
    # while True:
    #     try:
    #         main()
    #     except Exception as e:
    #         print(e)
    #         continue
    #     except KeyboardInterrupt:
    #         print("Exiting")
    #         break
