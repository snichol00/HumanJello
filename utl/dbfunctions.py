# Standard Lib
import sqlite3
from sqlite3 import connect
from re import search
from numbers import Number
# Flask Lib
from flask import current_app, g
from datetime import datetime

"""
    This module deals with interaction with the database
    Uses SQLite commands
"""


DB_FILE = "HumanJello.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

# setting up the database
def setup():
    # c.execute("DROP TABLE users;")
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashpassword TEXT NOT NULL,
                displayname TEXT,
                osis INTEGER,
                email TEXT,
                grade TEXT,
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
                admin BOOLEAN,
                saved TEXT
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
                cost TEXT,
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

#GENERAL FUNCTIONS--------------------------
def update_user(c, username, field, newvalue):
    c.execute("UPDATE users SET %s = '%s' WHERE username = '%s'" % (
                field,
                newvalue,
                username
            )
        )
    return "Success"

# gets a column of a given database given a conditional
def get(tbl_name, column, conditional=""):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("SELECT %s FROM %s %s" % (column, tbl_name, conditional))
    values = c.fetchall()
    c.close()
    return [list(value) for value in values]

#OPPORTUNITIES FUNCTIONS---------------------------
# initialize opportunity based on required inputs
def createOp(c, name, des, nine, ten, elev, twel):
    c.execute("INSERT INTO opportunities (name, description, gr9, gr10, gr11, gr12) VALUES (?, ?, ?, ?, ?, ?);", (name, des, nine, ten, elev, twel))
    c.execute("SELECT last_insert_rowid();")
    id = c.fetchone()
    #print("id: ", id[0])
    return id[0]

def editOp(c, id, name, des, nine, ten, elev, twel):
    c.execute("UPDATE opportunities SET name = ?, description = ?, gr9 = ?, gr10 = ?, gr11 = ?, gr12 = ?;", (name, des, nine, ten, elev, twel))


def getInterests(c, id):
    out = ""
    c.execute("SELECT events,academic,business,community_service,leadership,museums,nature,stem,humanities, scholarships FROM opportunities WHERE opid=?;", (id, ))
    arr = c.fetchone()
    print(arr)
    return arr

def getGrades(c, id):
    c.execute("SELECT gr9,gr10,gr11,gr12 FROM opportunities WHERE opid = ?;", (id, ))
    return c.fetchone()

#updates a field of opportunity based on id
def updateOp(c, id, field, new_val):
    print("UPDATE opportunities SET %s = '%s' WHERE opid = %s;" % (field, new_val, id))
    c.execute("UPDATE opportunities SET %s = '%s' WHERE opid = %s;" % (field, new_val, id))

def addInterest(c, id, interest):
    c.execute("UPDATE opportunities SET %s = True WHERE opid = %s;" % (interest, id))

def insertOp(c, name, int, des, link, cost, gra, loc, due, start, end, notes):
    c.execute("INSERT into opportunities (name, interests, description, link, cost, grades, location, duedate, posted, start_date, end_date, notes) VALUES(?, ?);", (name, int, des, link, cost, gra, loc, due, datetime.now(), start, end, notes))

def getAllOps(c):
    c.execute("SELECT * FROM opportunities;")
    all = c.fetchall()
    return all

def getOp(c, id):
    c.execute("SELECT * FROM opportunities WHERE opid = ?;", (id, ))
    return c.fetchone()

def deleteOp(c, id):
    c.execute("DELETE FROM opportunities WHERE opid = ?;", (id, ))

#STUDENT FUNCTIONS---------------------------
def addStudent(c, user, hashp, disp, osisNum, emailAcc, gra, inter):
    c.execute("INSERT into users (username, hashpassword, displayname, osis, email, grade, interests, admin) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (user, hashp, disp, osisNum, emailAcc, gra, inter, False))

def createStudent(c, user, hashp):
    c.execute("INSERT into users (username, hashpassword, admin) VALUES(?, ?, ?)", (user, hashp, False))

def getGrade(user):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("SELECT grade FROM users WHERE username = ?;", (user, ))
    return c.fetchone()

def setGrade(c, user, new_grade):
    c.execute("UPDATE users SET grade = ? WHERE username = ?;", (new_grade, user))

def getStuInfo(c, user):
    c.execute("SELECT username, displayname, osis, email, grade FROM users WHERE username = ?;", (user, ))
    return c.fetchone()

#return whether or not the student has filled in basic info yet
def studentInit(c, username):
    c.execute("SELECT * FROM users WHERE username = ?;", (username,))
    userinfo = c.fetchall()
    if userinfo[0][3]:
        return True
    return False

def getStudentInts(c, username):
    c.execute("SELECT events,academic,business,community_service,leadership,museums,nature,stem,humanities, scholarships FROM users WHERE username = ?;", (username, ))
    return c.fetchone()

def addStuInt(c, int, username):
    # print("UPDATE users SET %s = True WHERE username = %s" % (int, username))
    c.execute("UPDATE users SET %s = 1 WHERE username = '%s';" % (int, username))

def delStuInt(c, int, username):
    c.execute("UPDATE users SET %s = 0 WHERE username = '%s';" % (int, username))

#returns list of opids student has saved
def getStuSavedOpids(c, username):
    c.execute("SELECT saved FROM users WHERE username = ?;", (username, ))
    saved = c.fetchone()[0]
    if saved == None:
        return []
    out = saved.split(",")
    print(saved, out)
    return out

#gets list of students saved interests
def getStuSavedInts(c, username):
    opids = getStuSavedOpids(c, username)
    out = []
    for opid in opids:
        out.append(getOp(c, opid))
    return out

def stuSave(c, username, opid):
    c.execute("SELECT saved FROM users WHERE username = ?;", (username, ))
    saved = c.fetchone()[0]
    print(saved)
    if saved == None:
        saved = str(opid)
    else:
        saved = saved + "," + str(opid)
    print(saved)
    c.execute("UPDATE users SET saved = ? WHERE username = ?;", (saved, username))

def stuUnSave(c, username, opid):
    c.execute("SELECT saved FROM users WHERE username=?;", (username, ))
    saved = c.fetchone()[0]
    print("OLD SAVED", saved)
    saved = saved.replace(str(opid), "")
    saved = saved.replace(",,",",") #if extra comma
    if len(saved) > 1:
        if saved[0] == ",":
            saved = saved[1:]
        if saved[-1] == ",":
            saved = saved[0:-1]
    print("NEW SAVED", saved)
    c.execute("UPDATE users SET saved = ? WHERE username = ?;", (saved, username))

#ADMIN FUNCTIONS-----------------------------
def addAdmin(c, user, hashp, emailAcc):
    c.execute("INSERT INTO users (username, hashpassword, email, admin) VALUES(?, ?, ?, ?);", (user, hashp, emailAcc, True))

def isAdmin(c, username):
    c.execute("SELECT admin FROM users WHERE username = ?", (username, ))
    userinfo = c.fetchone()
    print(userinfo)
    return userinfo[0]
