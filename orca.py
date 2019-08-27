import argparse
import sqlite3
import csv
import json
from colorama import init, Fore

init()

# some constants
VERSION = "0.1"
DB_NAME = ":memory:"


# arguments parsing
parser = argparse.ArgumentParser(
    prog="Orca",
    description="Process .bash_history file via sqlite3 database.",
    epilog="""orca.py --process .bash_history_sample1 --count""",
)
parser.add_argument(
    "-p",
    "--process",
    help="process a .bash_history file into an sqlite db.",
    type=str,
    metavar="bash_history",
)
parser.add_argument(
    "-e",
    "--export",
    help="export .bash_history content into csv or json.",
    choices=["csv", "json"],
    metavar="format",
)
parser.add_argument(
    "-lc",
    "--lastcmd",
    help="print the last typed command in bash.",
    action="store_const",
    const=-1,
)
parser.add_argument(
    "-c",
    "--count",
    help="count the number of items in history.",
    action="store_const",
    const=-1,
)
parser.add_argument(
    "-l",
    "--list",
    help="list the items of bash history.",
    action="store_const",
    const=-1,
)
parser.add_argument(
    "-s", "--search", help="search for the term in the db.", type=str, metavar="term"
)
parser.add_argument(
    "-v",
    "--version",
    help="print the current script version",
    action="version",
    version=f"Version {VERSION}",
)
args = parser.parse_args()

conn = ""
if args.process:
    # print(args.process) # print a .bash_history

    # read lines of bash_history file
    f_bh = open(args.process)
    line_lst = []
    for line in f_bh:
        line_lst.append(line)
    f_bh.close()

    # create a DB in MEMORY and insert all values in it
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """ CREATE TABLE bash_history (id int, command text, UNIQUE(id,command) )"""
    )
    for i, line in enumerate(line_lst):
        c.execute(""" INSERT INTO bash_history VALUES (?,?)""", (i, line.rstrip("\n")))
    conn.commit()


if args.count:
    # print(args.count) # print -1 the value of const.

    # count the number of ids in table bash_history

    c = conn.cursor()
    c.execute(""" SELECT COUNT(id) FROM bash_history """)
    count = c.fetchone()[0]

    print(
        f"Number of items in {Fore.GREEN}{DB_NAME}{Fore.RESET} : {Fore.RED}{count}{Fore.RESET}"
    )

if args.list:
    # print(args.list)

    c = conn.cursor()
    c.execute(""" SELECT * FROM bash_history """)
    rows = c.fetchall()
    for row in rows:
        print(
            f"At {Fore.RED}{row[0]}{Fore.RESET} cmd --> {Fore.GREEN}{row[1]}{Fore.RESET}"
        )

if args.lastcmd:
    # print(args.lastcmd)

    c = conn.cursor()
    c.execute(""" SELECT * FROM bash_history """)
    rows = c.fetchall()
    lc = rows[len(rows) - 1]
    print(f"Last typed cmd --> {Fore.GREEN}{lc[1]}{Fore.RESET}")

if args.search:
    # print(args.search)

    c = conn.cursor()
    c.execute(""" SELECT * FROM bash_history """)  # , (args.search,))
    rows = c.fetchall()
    isFound = False
    for row in rows:
        if args.search in row[1]:
            print(
                f"Found {Fore.GREEN}{args.search}{Fore.RESET} at {Fore.RED}{row[0]}{Fore.RESET} cmd --> {Fore.GREEN}{row[1]}{Fore.RESET}"
            )
            isFound = True

    if not isFound:
        print(f"Command {Fore.GREEN}{args.search}{Fore.RESET} not found.")

if args.export:
    # print(args.export)

    if args.export == "csv":
        with open("exported.csv", 'w', newline='') as csvfile:
            export_writer = csv.writer(csvfile, delimiter=',', quotechar='\\') # TO BE FIXED

            # get content for DB in memory 
            c = conn.cursor()
            c.execute(""" SELECT * FROM bash_history """)  
            rows = c.fetchall()
            for row in rows: 
                export_writer.writerow([row[0],row[1]])

    elif args.export == "json":
        c = conn.cursor()
        c.execute(""" SELECT * FROM bash_history """)  
        rows = c.fetchall()
        with open("exported.json", 'w') as f:
            json.dump(rows, f)

if conn:
    conn.close()
