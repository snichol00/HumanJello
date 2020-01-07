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


DB_FILE = "data/database.db"

# setting up the database
def setup():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashpassword TEXT NOT NULL,
                displayname TEXT NOT NULL,
                OSIS INTEGER,
                email TEXT NOT NULL,
                grade TEXT,
                interests TEXT,
                admin BOOLEAN
                );""")
    c.execute("""CREATE TABLE IF NOT EXISTS opportunities (
                opid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                organization TEXT,
                position TEXT,
                interests TEXT,
                description TEXT,
                grades TEXT,
                location TEXT,
                duedate TEXT,
                posted TIMESTAMP,
                dates TEXT
                );""")
    )
    c.close()
