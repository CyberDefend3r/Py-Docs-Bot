# Python Reference Bot
A reddit.com bot that will return reference links for official python docs, online references, and youtube videos.  
  
The bot will lurk the [/r/learnpython](https://www.reddit.com/r/learnpython/) subreddit and read all comments looking for its keyword. When found the bot will reply to the comment with the requested links to documentation all nicely formatted in markdown.  
  
## Usage

**Invoke the bot with `!doc` keyword**  
All you need to do to invoke the bot is to use the `!doc` keyword followed by a comma seperated list of search terms. Example: `!doc sys.path, relative imports, import a module from a different directory`. The bot will determine if any of the search terms are part of the python standard library or if it should simply search google/youtube for references. Google and youtube both search with the query: `how to <search terms> 'python'` and select the top 3 results. For example, `!doc for loops` the google search would be `how to for loops 'python'`. The quotes around python tells google that python must be in the returned results.  
  
**NOTE:**  
- The keyword and search terms must be on its own line in your comment or it will be ignored by the bot.  
- Full method path is required if you want to return links to official python documentation and the paths are case sensitive. (Correct: `!doc pathlib.Path`, Incorrect: `!doc Path`). The exception is if you want to return python documentation for the entire module (`!doc pathlib`) and for built-in python functions like zip, map, filter, etc. because there is no chain for those functions.  
  
# Example
  
<u>**Original Post:**</u>  
  
```
How do I import a module that is not in the same directory as my script?

I cant figure out what I am doing wrong. Can anyone help point me in the right direction
```

<u>**Your Comment:**</u>  
  
```
Python will check PATH and the directory the script is in for imports. If it is not in either of those locations, you would need to add it to PATH,  
move it into the script directory or use relative imports.  
  
You can use sys.path to add the directory to path so that python will check that directory for imports.  
  
!doc sys.path, relative imports, import module from a different directory  
```  
  
<u>**Bot Reply to Your Comment:**</u>  
  

**Thanks for using the Python Reference Bot!**  
*For instructions on how to use me, check out my README on [GitHub](https://github.com/trevormiller6/Py-Reference)*  
  
# sys.path:

Official Documentation:  
- [sys — System-specific parameters and functions — Python 3.9.6 documentation](https://docs.python.org/3/library/sys.html#sys.path)

Online Resources:  
- [Python import, sys.path, and PYTHONPATH Tutorial | DevDungeon](https://www.devdungeon.com/content/python-import-syspath-and-pythonpath-tutorial)  
- [python - adding directory to sys.path /PYTHONPATH - Stack Overflow](https://stackoverflow.com/questions/16114391/adding-directory-to-sys-path-pythonpath)  
- [Where is Python's sys.path initialized from? - Stack Overflow](https://stackoverflow.com/questions/897792/where-is-pythons-sys-path-initialized-from)

Youtube Videos:  
- [Python Programming 53 - Sys.path and Changing Module Paths - YouTube](https://www.youtube.com/watch?v=5z5nALNandM)  
- [Sys.path.append Module Not Found Error solve it python - YouTube](https://www.youtube.com/watch?v=-aWN9FYfkFA)  
- [Python - Automatically add a module to syspath - YouTube](https://www.youtube.com/watch?v=dmH1AyQQu8s)  
  
# relative imports:

Online Resources:  
- [python - Relative imports for the billionth time - Stack Overflow](https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time)  
- [How to do relative imports in Python? - Stack Overflow](https://stackoverflow.com/questions/72852/how-to-do-relative-imports-in-python)  
- [Relative imports in Python 3 - Stack Overflow](https://stackoverflow.com/questions/16981921/relative-imports-in-python-3)

Youtube Videos:  
- [Python Import | Relative import | Import python File from Directory - YouTube](https://www.youtube.com/watch?v=X1cwEKfRZJE)  
- [HOW TO: Do Relative & Absolute Imports (Python Error Explained) - YouTube](https://www.youtube.com/watch?v=nk7UWUKlfGM)  
- [Python 3 Absolute and Relative Import - YouTube](https://www.youtube.com/watch?v=plm3Rj3E9DA)  
  
# import module from a different directory:

Online Resources:  
- [Python – Import module from different directory - GeeksforGeeks](https://www.geeksforgeeks.org/python-import-module-from-different-directory/)  
- [Absolute vs Relative Imports in Python â Real Python](https://realpython.com/absolute-vs-relative-python-imports/)  
- [Import modules in Python | Import module from different directory | Python Tutorial for beginners #5 - YouTube](https://www.youtube.com/watch?v=HNChkuE6HyA)

Youtube Videos:  
- [Python Import | Relative import | Import python File from Directory - YouTube](https://www.youtube.com/watch?v=X1cwEKfRZJE)  
- [Python Tutorial for Beginners 9: Import Modules and Exploring The Standard Library - YouTube](https://www.youtube.com/watch?v=CqvZ3vGoGs0)  
- [Absolute Imports in Python - YouTube](https://www.youtube.com/watch?v=qK3S5KoaRIg)  