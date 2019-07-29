import argparse

VERSION = "0.1"

# arguments parsing 
parser = argparse.ArgumentParser(prog='bh2db', description="Process .bash_history file via sqlite3 database.")
group = parser.add_mutually_exclusive_group()
group.add_argument('-p', "--process", help="process a .bash_history file into an sqlite db.", type=str, metavar='bash_history')
group.add_argument('-i', "--import", help="import a sqlite db file.", type=str, metavar='file.db')
parser.add_argument('-e', "--export", help="export .bash_history content into csv format.", choices=['csv', 'json', 'text'], metavar='format')
parser.add_argument('-lc', "--last-cmd", help="print the last typed command in bash.", action='store_const', const=-1)
parser.add_argument('-c', "--count", help="count the number of items in history.", action='store_const', const=-1)
parser.add_argument('-s', "--search",  help="search for the term in the db.", type=str, metavar='term')
parser.add_argument('-v', "--version", help="print the current script version", action='version', version=f"Version {VERSION}")
args = parser.parse_args()

if args.process:
    print(args.process) # print a .bash_history
    
    f_bh = open(args.process)
    print(f_bh.readline().strip().split('  '))
    f_bh.close()



if args.search:
    print(args.search)

if args.count:
    print(args.count) # print -1 the value of const.



    # There is a little misunderstanding here, history does not show the content of ~/.bash_history. 
    # Instead, it shows the current content of Bash's history list in memory for this session.