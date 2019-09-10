import argparse
import sqlite3
import csv
import json
from colorama import init, Fore

init()

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  connect ORM to sqlite using a memory engine
DB_NAME = "sqlite:///:memory:"
engine = create_engine(DB_NAME, echo=False)
Base = declarative_base()


class Bash_history(Base):
    __tablename__ = "bash_histories"

    id = Column(Integer, primary_key=True)
    command = Column(String)

    def __repr__(self):
        return f"Bash_history({self.id} - {self.command})."


# some constants
VERSION = "0.1"

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

conn = None
if args.process:
    # print(args.process) # print a .bash_history

    # read lines of bash_history file
    f_bh = open(args.process)
    line_lst = []
    for line in f_bh:
        line_lst.append(line)
    f_bh.close()

    # create a DB in MEMORY and insert all values in it
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    for line in line_lst:
        bash_history = Bash_history(command=line.rstrip("\n"))
        session.add(bash_history)
    session.commit()


if args.count:
    # print(args.count) # print -1 the value of const.

    # count the number of commands in table bash_histories table
    count = session.query(Bash_history).count()
    print(
        f"Number of items in {Fore.GREEN}{DB_NAME}{Fore.RESET}: {Fore.RED}{count}{Fore.RESET}"
    )

if args.list:
    # print(args.list)

    rows = session.query(Bash_history).all()
    for row in rows:
        print(
            f"At {Fore.RED}{row.id}{Fore.RESET} cmd --> {Fore.GREEN}{row.command}{Fore.RESET}"
        )

if args.lastcmd:
    # print(args.lastcmd)

    row = session.query(Bash_history).order_by(Bash_history.id.desc()).first()
    print(f"Last typed cmd --> {Fore.GREEN}{row.command}{Fore.RESET}")

if args.search:
    # print(args.search)

    rows = session.query(Bash_history).filter(Bash_history.command.like(f"%{args.search}%"))

    isFound = False
    for row in rows:
        print(f"Found {Fore.GREEN}{args.search}{Fore.RESET} at {Fore.RED}{row.id}{Fore.RESET} cmd --> {Fore.GREEN}{row.command}{Fore.RESET}")
        isFound = True

    if not isFound:
        print(f"Command {Fore.GREEN}{args.search}{Fore.RESET} not found.")

if args.export:
    # print(args.export)

    if args.export == "csv":
        with open("exported.csv", "w", newline="") as csvfile:
            export_writer = csv.writer(
                csvfile, delimiter=",", quotechar="\\"
            )  #  TO BE FIXED

            #  get content for DB in memory
            rows = session.query(Bash_history).all()
            for row in rows:
                export_writer.writerow([row.id, row.command])

    elif args.export == "json":
        rows = session.query(Bash_history).all()
        d_to_json = dict()
        for row in rows:
            d_to_json[row.id] = row.command
        with open("exported.json", "w") as f:
            json.dump(d_to_json, f)

if conn:
    conn.close()
