[![Pylint & flake8](https://github.com/trevormiller6/Py-Docs-Bot/actions/workflows/flakelint.yml/badge.svg)](https://github.com/trevormiller6/Py-Docs-Bot/actions/workflows/flakelint.yml) [![CodeQL](https://github.com/trevormiller6/Py-Docs-Bot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/trevormiller6/Py-Docs-Bot/actions/workflows/codeql-analysis.yml)  
# Python Docs Bot
A reddit.com bot that will return documentation links for the library and language reference sections of the python docs website. The bot can also return links to python pep documentation. The bot monitors the [r/learnpython](https://www.reddit.com/r/learnpython/) subreddit's comments looking for its keyword. When found the bot will reply to the comment with the requested links to documentation.  
  
## Usage

**Invoke the bot with `!docs` keyword**  
  
All you need to do is use the `!docs` keyword followed by a comma seperated list of search terms anywhere in your comment as long as it's on its own line.  
  
**Examples:**
```
!docs os.path, pathlib.Path
```   
Returns library reference documentation links to os.path and pathlib.Path.  
```  
!docs function, class
```  
Returns python language reference links for function definitions and class definitions.    
```
!docs while, input
```
Returns language reference for while statement and a library reference for the input function.  
```
!docs pep-20, pep-8
```
Returns links to pep-20 "The Zen of Python" and pep-8 "Style Guide for Python Code"
  
**Important**  
- To prevent the bot from spamming posts, the bot will not reply if it clouldn't find a valid documentation link based on your search terms. It will silently ignore the request.  
  
- The keyword and search terms must be on its own line in your comment or it will be ignored by the bot.  
  
- Full method path is required and the paths are case sensitive for **standard library references only** (Correct: `!docs pathlib.Path`, Incorrect: `!docs pathlib.path`, or `!docs Path`). This is for a few reasons but the biggest one is that it allows the bot to include page anchors in the links. This way if someone is recommending Path from pathlib and sent them the link to pathlib library docs they would have to scroll through all the other methods searching for Path. Page anchors solve that.  
  - Exceptions to needing the full method path:
    - You want to return python documentation for the entire module (Correct: `!docs pathlib`) 
    - Built-in python functions like zip, map, filter, etc. because there is no chain for those functions (Correct: `!docs filter`).  
  
- Python language references are found by doing basically a keyword search against all the items on its index page (linked below). For example, `!docs while` would return a link to the language reference page titled "[The while statement](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)"  
  
Refer to these links to see what the bot can return.  
  - [Python Language Reference - https://docs.python.org/3/reference/index.html](https://docs.python.org/3/reference/index.html)  
  - [Python Library Reference - https://docs.python.org/3/library/index.html](https://docs.python.org/3/library/index.html)  
  - [Python Enhancement Proposals - https://www.python.org/dev/peps/](https://www.python.org/dev/peps/)
  
All links created and distributed by the bot link back to [https://docs.python.org](https://docs.python.org) and [https://www.python.org/dev/peps/](https://www.python.org/dev/peps/) and no where else.  
  
# Full Example
  
Below is an example of how to use the bot. I have tried to make it super simple to use. If you are still unsure of how to use it you can [checkout the bot's reddit profile](https://www.reddit.com/user/py_reference_bot) and see how others have used the bot by reviewing the comments it has replied to.  
  
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
  
Python Documentation Bot - *[How To Use](https://github.com/trevormiller6/Py-Docs-Bot)*
  
----  
<img src="https://cdn.cdnlogo.com/logos/t/48/twitter.png" width="20px"> [@Cyb3rDefender](https://twitter.com/Cyb3rDefender)
