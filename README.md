# BashHistory2SQLITE
Bash History 2 SQLITE : Process .bash_history file via sqlite3 database.

# Usage :

```
usage: bh2db [-h] [-p bash_history | -i file.db] [-c] [-s term] [-v]

optional arguments:
  -h, --help                               show this help message and exit
  -p bash_history, --process bash_history  process a .bash_history file into an sqlite db.
  -i file.db, --import file.db             import a sqlite db file.
  -c, --count                              count the number of items in history.
  -s term, --search term                   search for the term in the db.
  -v, --version                            print the current script version
  ```
