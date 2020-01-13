# Standard Lib
import sqlite3
from sqlite3 import connect
from re import search
from numbers import Number
# Flask Lib
from flask import current_app, g

# should return all opportunities relevant to the user
def relOps(userID):
    opList = []
    for opID in opportunities:
        if (isOpRel(opID, userID)):
            opList.append(opID)
    return opList

# should return whether the opportunity is of interest to the given user
def isOpRel(opID, userID):
    if 
