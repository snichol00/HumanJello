# Standard Lib
import sqlite3
from sqlite3 import connect
from re import search
from numbers import Number
# Flask Lib
from flask import current_app, g
import dbfunctions

# should return all opportunities relevant to the user
def relOps(username):
    opList = []
    opportunities = getAllOps(c)
    for opID in opportunities:
        if (isOpRel(opID, username)):
            opList.append(opID)
    return opList

# should return whether the opportunity is of interest to the given user
def isOpRel(opID, username):
    opAc = get("opportunities", "academic", "WHERE opid = '%s'" % opID)[0][0]
    opBu = get("opportunities", "business", "WHERE opid = '%s'" % opID)[0][0]
    opCo = get("opportunities", "community_service", "WHERE opid = '%s'" % opID)[0][0]
    opLe = get("opportunities", "leadership", "WHERE opid = '%s'" % opID)[0][0]
    opMu = get("opportunities", "museums", "WHERE opid = '%s'" % opID)[0][0]
    opNa = get("opportunities", "nature", "WHERE opid = '%s'" % opID)[0][0]
    opSt = get("opportunities", "stem", "WHERE opid = '%s'" % opID)[0][0]
    opHu = get("opportunities", "humanities", "WHERE opid = '%s'" % opID)[0][0]
    opSc = get("opportunities", "scholarships", "WHERE opid = '%s'" % opID)[0][0]

    sAc = get("users", "academic", "WHERE username = '%s'" % username)[0][0]
    sBu = get("users", "business", "WHERE username = '%s'" % username)[0][0]
    sCo = get("users", "community_service", "WHERE username = '%s'" % username)[0][0]
    sLe = get("users", "leadership", "WHERE username = '%s'" % username)[0][0]
    sMu = get("users", "museums", "WHERE username = '%s'" % username)[0][0]
    sNa = get("users", "nature", "WHERE username = '%s'" % username)[0][0]
    sSt = get("users", "stem", "WHERE username = '%s'" % username)[0][0]
    sHu = get("users", "humanities", "WHERE username = '%s'" % username)[0][0]
    sSc = get("users", "scholarships", "WHERE username = '%s'" % username)[0][0]

    if (opAc != sAc and opBu != sBu and opCo != sCo and opLe != sLe and opMu != sMu
        and opNa != sNa and opSt != sSt and opHu != sHu and opSc != sSc):
        return False

    opNine = get("opportunities", "gr9", "WHERE opid = '%s'" % opID)[0][0]
    opTen = get("opportunities", "gr10", "WHERE opid = '%s'" % opID)[0][0]
    opEleven = get("opportunities", "gr11", "WHERE opid = '%s'" % opID)[0][0]
    opTwelve = get("opportunities", "gr12", "WHERE opid = '%s'" % opID)[0][0]
    sGrade = get("users", "grade", "WHERE username = '%s'" % username)[0][0]

    if (grade == "9" and !opNine):
        if (grade == "10" and !opTen):
            if (grade == "11" and !opEleven):
                if (grade == "12" and !opTwelve):
                    return False;

    return True
