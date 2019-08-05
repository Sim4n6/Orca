import argparse
import sqlite3

VERSION = "0.1"

# arguments parsing 
parser = argparse.ArgumentParser(prog='bh2db', description="Process .bash_history file via sqlite3 database.")
group = parser.add_mutually_exclusive_group()
group.add_argument('-p', "--process", help="process a .bash_history file into an sqlite db.", type=str, metavar='bash_history')
group.add_argument('-lo', "--load", help="load a sqlite db file.", type=str, metavar='file.db')
parser.add_argument('-e', "--export", help="export .bash_history content into csv | json | text format.", choices=['csv', 'json', 'text'], metavar='format')
parser.add_argument('-lc', "--lastcmd", help="print the last typed command in bash.", action='store_const', const=-1)
parser.add_argument('-c', "--count", help="count the number of items in history.", action='store_const', const=-1)
parser.add_argument('-l', "--list", help="list the items of bash history.", action='store_const', const=-1)
parser.add_argument('-s', "--search",  help="search for the term in the db.", type=str, metavar='term')
parser.add_argument('-v', "--version", help="print the current script version", action='version', version=f"Version {VERSION}")
args = parser.parse_args()

if args.process:
    print(args.process) # print a .bash_history
    
    # read lines of bash_history file
    f_bh = open(args.process)
    tokens_lst = []
    for line in f_bh :
        tokens = line.strip().split('  ')
        print(tokens[0], tokens[1])
        tokens_lst.append(tokens)
    f_bh.close()

    # create a DB and insert all values in it
    conn = sqlite3.connect("bash_history.db")
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS bash_history (ids int, commands text, UNIQUE(ids, commands))""")
    for tokens in tokens_lst:
        c.execute(""" INSERT OR IGNORE INTO bash_history VALUES (?,?)""",(tokens[0],tokens[1]))
    conn.commit()
    conn.close()

if args.load:
    print(args.load)

    conn = sqlite3.connect(args.load)
    c = conn.cursor()
    conn.close()

if args.count:
    print(args.count) # print -1 the value of const.

    # count the number of ids in table bash_history
    conn = sqlite3.connect("bash_history.db")
    c = conn.cursor()
    c.execute(""" SELECT COUNT(ids) FROM bash_history """)
    count = c.fetchone()[0]
    conn.close()

    print(f"Number of items in bash_history.db : {count}")

if args.list:
    print(args.list)

    conn = sqlite3.connect("bash_history.db")
    c = conn.cursor()
    c.execute(""" SELECT * FROM bash_history """)
    rows = c.fetchall()
    for row in rows : 
        print(f"At {row[0]} cmd --> {row[1]}")
    conn.close()

if args.lastcmd:
    print(args.lastcmd)

    conn = sqlite3.connect("bash_history.db")
    c = conn.cursor()
    c.execute(""" SELECT * FROM bash_history """)
    rows = c.fetchall()
    lc = rows[len(rows)-1]
    print(f"Last typed cmd --> {lc[1]}")
    conn.close()


if args.search:
    print(args.search)

    conn = sqlite3.connect("bash_history.db")
    c = conn.cursor()
    c.execute(""" SELECT * FROM bash_history WHERE commands = ?""",(args.search,))
    rows = c.fetchall()
    if len(rows) != 0:
        for row in rows : 
            print(f"At {row[0]} cmd --> {row[1]}")
    else:
        print("Command not found")
    conn.close()


    # There is a little misunderstanding here, history does not show the content of ~/.bash_history. 
    # Instead, it shows the current content of Bash's history list in memory for this session.