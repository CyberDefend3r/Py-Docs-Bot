# Python Docs Bot
A reddit.com bot that will return documentation links for the python library and language reference sections of the python docs website.  
  
The bot will monitor the [r/learnpython](https://www.reddit.com/r/learnpython/) subreddit's comments looking for its keyword. When found the bot will reply to the comment with the requested links to documentation.  
  
## Usage

**Invoke the bot with `!docs` keyword**  
- All you need to do is use the `!docs` keyword followed by a comma seperated list of search terms.  
```
!docs os.path, pathlib.Path
```   
Returns links to os.path and pathlib.Path python library reference documentation.  
```  
!docs function, class
```  
Returns python language reference links for function definitions and class definitions.  
  
**Important**  
- To prevent the bot from spamming posts, the bot will not reply if it clouldn't find a valid documentation link based on your search terms. It will silently ignore the request.  
  
- The keyword and search terms must be on its own line in your comment or it will be ignored by the bot.  
  
- Full method path is required and the paths are case sensitive. **library references only.** (Correct: `!docs pathlib.Path`, Incorrect: `!docs pathlib.path`, or `!docs Path`). 
  - Exceptions to needing the full method path:
    - You want to return python documentation for the entire module (Correct: `!docs pathlib`) 
    - Built-in python functions like zip, map, filter, etc. because there is no chain for those functions (Correct: `!docs filter`).  
  
- Language references are found by doing a fuzzy search using the search term provided, so searches are not case sensitive like library references are.  
  
- The bot can tell if you are requesting a language or library reference so mixing the two is fine in the same search.  
```
!docs while, input
```
Returns language reference for while statement and a library reference for the input function.  
  
To know the difference between the library and language references see the following two links. Though knowing what is provided in them is not necessary to use the bot. This is where all links created by the bot link too.  
  - [Python Language Reference](https://docs.python.org/3/reference/index.html)  
  - [Python Library Reference](https://docs.python.org/3/library/index.html)  
  
# Example
  
Below is an example of how to use the bot, if you are still confused [checkout the bot's reddit profile](https://www.reddit.com/user/py_reference_bot) and see how others have used the bot by seeing its replies.  
  
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
  
[sys.path - https://docs.python.org/3/library/sys.html#sys.path](https://docs.python.org/3/library/sys.html#sys.path)  
  
Python Documentation Bot - *[GitHub](https://github.com/trevormiller6/Py-Docs-Bot)*
