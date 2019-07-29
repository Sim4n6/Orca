import argparse

VERSION = "0.1"

parser = argparse.ArgumentParser(prog='bh2db', description="Process .bash_history file via sqlite3 database.")
group = parser.add_mutually_exclusive_group()
group.add_argument('-p', "--process", help="process a .bash_history file into an sqlite db.", type=str, metavar='bash_history')
group.add_argument('-i', "--import", help="import a sqlite db file.", type=str, metavar='file.db')
parser.add_argument('-c', "--count", help="count the number of items in history.", action='store_const', const=-1)
parser.add_argument('-s', "--search",  help="search for the term in the db.", type=str, metavar='term')
parser.add_argument('-v', "--version", help="print the current script version", action='version', version=f"Version {VERSION}")
args = parser.parse_args()

if args.search:
    print(args.search)

if args.count:
    print(args.count) # print -1 the value of const.