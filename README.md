# Orca
 <img src="orca.png" /> **Orca** a cmdline tool to process .bash_history file using SQLite db. 

### Usage :

```
usage: Orca [-h] [-p .bash_history | -lo file.db] [-e format] [-lc] [-c] [-l] [-s term] [-v]

Process .bash_history file via sqlite3 database.

optional arguments:
  -h, --help            show this help message and exit
  -p bash_history, --process bash_history
                        process a .bash_history file into an sqlite db.
  -lo file.db, --load file.db
                        load a sqlite db file.
  -e format, --export format
                        export .bash_history content into csv | json | text
                        format.
  -lc, --lastcmd        print the last typed command in bash.
  -c, --count           count the number of items in history.
  -l, --list            list the items of bash history.
  -s term, --search term
                        search for the term in the db.
  -v, --version         print the current script version

Examples : 
   orca.py --process Samples\.bash_history1 --count 
   orca.py --load bash_history.db --lastcmd
  ```

