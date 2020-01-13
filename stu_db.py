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
