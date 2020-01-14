# Standard Lib
import sqlite3
from sqlite3 import connect
from re import search
from numbers import Number
# Flask Lib
from flask import current_app, g

DB_FILE = "HumanJello.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

# insert an opportunity into the database
def insertOp(c, org, pos, int, des, gra, loc, due, post, dat):
    c.execute("INSERT into opportunities (organization, position, interests, description, grades, location, duedate, posted, dates) VALUES(?, ?);", (org, pos, int, des, gra, loc, due, pos, dat))

def getOp():
    c.execute("SELECT name FROM opportunities;")
    # https://getbootstrap.com/docs/4.4/components/collapse/
    # https://getbootstrap.com/docs/4.4/components/breadcrumb/
