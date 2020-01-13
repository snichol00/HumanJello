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
    opGrades = get("opportunities", "grades", "WHERE opid = '%s'" % opID)[0][0]
    sGrade = get("users", "grades", "WHERE userid = '%s'" % userID)[0][0]
    matches = 0
    for grade in opGrades:
        if (sGrade == grade):
            matches ++
    if (matches == 0):
        return False

    opInterests = get("opportunities", "interests", "WHERE opid = '%s'" % opID)[0][0]
    sInterests = get("users", "interests", "WHERE userid = '%s'" % userID)[0][0]
    same = 0
    for interestO in opInterests:
        for interestS in sInterests:
            if (interestO == interestS):
                same ++
    if (same == 0):
        return False

    return True
