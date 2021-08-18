# Python Reference Bot
A reddit.com bot that will return reference links for official python docs, online references, and youtube videos.  
  
The bot will lurk the [/r/learnpython](https://www.reddit.com/r/learnpython/) subreddit and read all comments looking for its keywords. When found the bot will reply to the comment with the requested links to documentation all nicely formatted in markdown.  
  
## Usage
**Make sure to READ and UNDERSTAND the `NOTE` section!**
  
### !py-official
This command will tell the bot to reply with links to the official python documentation found at https://docs.python.org/3/library/  
  
### !py-refs
This command will tell the bot to reply with links for official python documentation, online resources, and youtube videos.  
  
### !py-howto
This command will tell the bot to reply with links to online resources and youtube videos.  
These links are gatheresd by doing a google search with the query: `how to <search terms> 'python'` and selecting the top 3 results. For example, `!py-howto for loops` the the google search would be `how to for loops 'python'`.  
  
**NOTE:**  
* Full method chain is required for input if making a request with either `!py-refs` or `!py-official` and the module paths are case sensitive (ex. `pathlib.Path`).  
* The command and arguments must be on its own line in your comment or it will be ignored.  
* When requesting more than one item, they need to be seperated by a comma with a space. EX. `!py-official pathlib.Path, re.search, configparser`  
* When requesting references for built-in python functions like zip, map, filter, etc you need to prepend the function with the word `function`. EX `!py-official function.zip, function.enumerate, function.classmethod`. This is because of the url paths for the python documentation site.
  
## Example
  
**command:**  
  
`!py-refs os.path`  
  
**Output:**  
  
**Thanks for using the Python Reference Bot!**  
If you think my references were helpful please upvote!  
*For a list of available commands, check out my [GitHub](https://github.com/trevormiller6/Py-Reference)*  
  
# os.path:

Official Documentation:  
- [os.path - Common pathname manipulations - Python 3.9.6 documentation](https://docs.python.org/3/library/os.path.html#os.path)

Online Resources:  
- [OS Path module in Python - GeeksforGeeks](https://www.geeksforgeeks.org/os-path-module-python/)  
- [Python | os.path.join() method - GeeksforGeeks](https://www.geeksforgeeks.org/python-os-path-join-method/)  

Youtube Videos:  
- [Python OS Path - YouTube](https://www.youtube.com/watch?v=jGjnOoBH4Wk)  
- [Python 12 - OS Path - YouTube](https://www.youtube.com/watch?v=JnaI-s9ehfI)  
- [Working with Os Path Module - Python Advanced Tutorial Series - 52 - YouTube](https://www.youtube.com/watch?v=oScYBpcVM4Y)  
