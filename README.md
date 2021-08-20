# Python Docs Bot
A reddit.com bot that will return documentation links for the python standard library  
  
The bot will monitor the [/r/learnpython](https://www.reddit.com/r/learnpython/) subreddit's comments looking for its keyword. When found the bot will reply to the comment with the requested links to documentation.  
  
## Usage

**Invoke the bot with `!docs` keyword**  
- All you need to do is use the `!docs` keyword followed by a comma seperated list of search terms.  
```
!docs os.path, pathlib.Path
```   
  
**Important**  
- To prevent the bot from spamming posts, the bot will not reply if it clouldn't find a valid documentation link based on your search terms. It will silently ignore the request.  
  
- The keyword and search terms must be on its own line in your comment or it will be ignored by the bot.  
  
- Full method path is required and the paths are case sensitive. (Correct: `!docs pathlib.Path`, Incorrect: `!docs pathlib.path`, or `!docs Path`). The exceptions are if you want to return python documentation for the entire module (`!docs pathlib`) and built-in python functions like zip, map, filter, etc. because there is no chain for those functions (`!docs map, filter`).  
  
# Example
  
**Original Post:**  
  
```
How do I import a module that is not in the same directory as my script?

I cant figure out what I am doing wrong. Can anyone help point me in the right direction
```

**Your Comment:**  
  
```
Python will check PYTHONPATH and the directory the script is in for imports. If it is not in those locations,  
you would need to do one of the following:  
    1) add it to PYTHONPATH  
    2) move it into the script directory  
    3) use relative imports  
  
You can use sys.path to add the directory to PATH so that python will check that directory for imports.  
  
!docs sys.path  
```    
  
**Bot's Reply to Your Comment:**  
  
---
  
Python Docs:  
[sys.path - https://docs.python.org/3/library/sys.html#sys.path](https://docs.python.org/3/library/sys.html#sys.path)  
  
Python Reference Bot - *[GitHub](https://github.com/trevormiller6/Py-Docs-Bot)*