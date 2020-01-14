# Standard Lib
import sqlite3
from sqlite3 import connect
from re import search
from numbers import Number
# Flask Lib
from flask import current_app, g

"""
    This module deals with interaction with the database
    Uses SQLite commands
"""


DB_FILE = "HumanJello.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

# setting up the database
def setup():
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashpassword TEXT NOT NULL,
                displayname TEXT,
                osis INTEGER,
                email TEXT,
                grade TEXT,
                academic BOOLEAN,
                business BOOLEAN,
                community_service BOOLEAN,
                leadership BOOLEAN,
                museums BOOLEAN,
                nature BOOLEAN,
                stem BOOLEAN,
                humanities BOOLEAN,
                scholarships BOOLEAN,
                admin BOOLEAN
                );""")
    c.execute("""CREATE TABLE IF NOT EXISTS opportunities (
                opid INTEGER PRIMARY KEY,
                name TEXT,
                events BOOLEAN,
                academic BOOLEAN,
                business BOOLEAN,
                community_service BOOLEAN,
                leadership BOOLEAN,
                museums BOOLEAN,
                nature BOOLEAN,
                stem BOOLEAN,
                humanities BOOLEAN,
                scholarships BOOLEAN,
                description TEXT,
                link TEXT,
                cost INTEGER,
                gr9 BOOLEAN,
                gr10 BOOLEAN,
                gr11 BOOLEAN,
                gr12 BOOLEAN,
                location TEXT,
                duedate TEXT,
                posted TEXT,
                start_date TEXT,
                end_date TEXT,
                notes TEXT
                );""")

# initialize opportunity based on required inputs
def createOp(c, name, des, nine, ten, elev, twel):
    c.execute("INSERT INTO opportunities (name, description, gr9, gr10, gr11, gr12) VALUES (?, ?, ?, ?, ?, ?);", (name, des, nine, ten, elev, twel))
    c.execute("SELECT last_insert_rowid();")
    id = c.fetchone()
    #print("id: ", id[0])
    return id[0]

def addInterest(c, id, interest):
    c.execute("UPDATE opportunities SET %s = True WHERE opid = %d;" % (interest, id))

def insertOp(c, name, int, des, link, cost, gra, loc, due, start, end, notes):
    c.execute("INSERT into opportunities (name, interests, description, link, cost, grades, location, duedate, posted, start_date, end_date, notes) VALUES(?, ?);", (name, int, des, link, cost, gra, loc, due, datetime('now'), start, end, notes))

def addStudent(c, user, hashp, disp, osisNum, emailAcc, gra, inter):
    c.execute("INSERT into users (username, hashpassword, displayname, osis, email, grade, interests, admin) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (user, hashp, disp, osisNum, emailAcc, gra, inter, False))

def createStudent(c, user, hashp):
    c.execute("INSERT into users (username, hashpassword, admin) VALUES(?, ?, ?)", (user, hashp, False))


def addAdmin(c, user, hashp, emailAcc):
    c.execute("INSERT INTO users (username, hashpassword, email, admin) VALUES(?, ?, ?, ?);", (user, hashp, emailAcc, True))

def isAdmin(c, username):
    c.execute("SELECT admin FROM users WHERE username = ?", (username, ))
    userinfo = c.fetchone()
    print(userinfo)
    return userinfo[0]

def update_user(c, username, field, newvalue):
    c.execute("UPDATE users SET %s = '%s' WHERE username = '%s'" % (
                field,
                newvalue,
                username
            )
        )
    return "Success"

#return whether or not the student has filled in basic info yet
def studentInit(c, username):
    c.execute("SELECT * FROM users WHERE username = ?;", (username,))
    userinfo = c.fetchall()
    if userinfo[0][3]:
        return True
    return False

# gets a column of a given database given a conditional
def get(tbl_name, column, conditional=""):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("SELECT %s FROM %s %s" % (column, tbl_name, conditional))
    values = c.fetchall()
    c.close()
    return [list(value) for value in values]
