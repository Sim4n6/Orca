import argparse

parser = argparse.ArgumentParser(description="Process .bash_history via sqlite3 db")
parser.add_argument("--import", '-i', help="import a db file", type=str, metavar='db')
parser.add_argument("--search", "-s", help="search for the term", type=str, metavar='term')
parser.add_argument("--count",'-c', help="count items in history")
parser.add_argument("--version","-v", help="print current script version")
args = parser.parse_args()

if args.search:
    print(args.search)
