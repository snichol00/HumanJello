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
                interests TEXT,
                admin BOOLEAN
                );""")
    c.execute("""CREATE TABLE IF NOT EXISTS opportunities (
                opid INTEGER PRIMARY KEY AUTOINCREMENT,
                organization TEXT,
                position TEXT,
                interests TEXT,
                description TEXT,
                grades TEXT,
                location TEXT,
                duedate TEXT,
                posted TEXT,
                dates TEXT
                );""")

# insert an opportunity into the database
def insertOp(c, org, pos, int, des, gra, loc, due, post, dat):
    c.execute("INSERT into opportunities (organization, position, interests, description, grades, location, duedate, posted, dates) VALUES(?, ?);", (org, pos, int, des, gra, loc, due, pos, dat))

def addStudent(c, user, hashp, disp, osisNum, emailAcc, gra, inter):
    c.execute("INSERT into users (username, hashpassword, displayname, osis, email, grade, interests, admin) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (user, hashp, disp, osisNum, emailAcc, gra, inter, False))

def createStudent(c, user, hashp):
    c.execute("INSERT into users (username, hashpassword, admin) VALUES(?, ?, ?)", (user, hashp, False))


def addAdmin(c, user, hashp, emailAcc):
    c.execute("INSERT INTO users (username, hashpassword, email, admin) VALUES(?, ?);", (user, hasp, email, True))


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
    c.execute("SELECT FROM users WHERE username = ?;", (username,))
    userinfo = c.fetchall()
    if userinfo[0][3]:
        return True
    return False
