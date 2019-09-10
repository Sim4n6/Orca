# Orca
 <img src="orca.png" /> **Orca** a cmdline tool to process .bash_history file using SQLite dbms and SQLalchemy. 

### Usage :

```
usage: Orca [-h] [-p bash_history] [-e format] [-lc] [-c] [-l] [-s term] [-v]

Process .bash_history file via sqlite3 database.

optional arguments:
  -h, --help            show this help message and exit
  -p bash_history, --process bash_history
                        process a .bash_history file into an sqlite db.
  -e format, --export format
                        export .bash_history content into csv or json.
  -lc, --lastcmd        print the last typed command in bash.
  -c, --count           count the number of items in history.
  -l, --list            list the items of bash history.
  -s term, --search term
                        search for the term in the db.
  -v, --version         print the current script version

Examples: 
    orca.py --process .bash_history_sample1 --count
    orca.py --process .bash_history_sample1 -lc -s "curl" -c
```

### NOTE :

There is a little misunderstanding. history cmd in Gnu/linux does not show the content file of ~/.bash_history.
Instead, it shows the current content of Bash's history list in memory for the current session.

