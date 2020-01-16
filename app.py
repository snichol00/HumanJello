from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from flask import Flask, render_template, redirect, url_for, session, flash, request
import json, sys
import sqlite3, os
from datetime import datetime
import urllib.request as urlrequest
from urllib.request import urlopen, Request
import dbfunctions
# from utl/fikter import relOps

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "HumanJello.db"
ADMIN_CODE = "admin"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

"""Setup databases"""
# open if file exists, otherwise create
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()  # facilitate db operations
dbfunctions.setup()

@app.route("/")
def root():
    if checkAuth(): #if logged in alrdy (cookies)
        if isAdmin():
            return redirect(url_for('adminHome'))
        #if student alrdy initialized, go to student home
        if dbfunctions.studentInit(c, session['username']):
            return redirect(url_for('studentHome'))
        #student needs to initialize
        return redirect(url_for('studentInfo'))
    return render_template("root.html")

def checkAuth(): #checks if the user is logged in
    if "username" in session:
        return True
    else:
        return False

def isAdmin():
    return session['admin']

#REDIRECT TO STUDENT/ADMIN REGISTER PAGE
@app.route("/studentAccount")
def studacc():
    return render_template("register.html", student=True)

@app.route("/adminAccount")
def adminacc():
    return render_template("register.html", admin=True)

#PAGE FOR STUDENT TO ENTER INFORMATION AFTER REGISTERING
@app.route("/studentInfo")
def studentInfo():
    if checkAuth() and not isAdmin():
        return render_template("studentinfo.html", user=session['username'])

#PROCESSES STUDENT INFORMATION
@app.route("/createStudent", methods=["POST"])
def createStudent():
    if request.method=="POST":
        username = session['username']
        print(request.form)
        displayname = request.form['displayname']
        grade = request.form['grade']
        osis = request.form['osis']
        email = request.form['email']
        dbfunctions.update_user(c, username, "grade", grade)
        dbfunctions.update_user(c, username, "osis", osis)
        dbfunctions.update_user(c, username, "email", email)
        dbfunctions.update_user(c, username, "displayname", displayname)
        db.commit()
    return redirect(url_for('studentHome'))

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        #determine if person registering was student or admin
        if 'adminCode' in request.form:
            admin = True
            register_route = 'studentacc'
        else:
            admin=False
            register_route = 'adminacc'
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        # TODO: Finish next line
        c.execute("SELECT username FROM users WHERE username = ?", (username, ))
        a = c.fetchone()
        if a is not None:  # checks for duplicate usernames
            flash("Account with that username already exists")
            return redirect(url_for(register_route))
        elif " " in username:  # checks for spaces cause spaces suck
            flash("Username cannot contain spaces")
            return redirect(url_for(register_route))
        elif password != password2:  # checks if both passwords are the same
            flash("Passwords do not match")
            return redirect(url_for(register_route))
        elif len(password) < 8:  # passwords must have a minimum length of 8
            flash("Password must be at least 8 characters in length")
            return redirect(url_for(register_route))
        #passwords do match
        else:  # successfully created an account
            if not admin:
                dbfunctions.createStudent(c, username, password)
                db.commit()
                flash("Successfuly created user")
                return redirect(url_for('login'))
            #below scenarios are for admin
            elif request.form['adminCode'] == ADMIN_CODE:  #if admin code matches, create account
                dbfunctions.addAdmin(c, username, password, request.form['email'])
                flash("Successfuly created user")
                db.commit()
                return redirect(url_for('login'))
            else:
                flash("Incorrect Admin Code")
                return redirect(url_for(register_route))

    else:
        flash("GET request")
        return redirect(url_for('root'))

@app.route("/login")
def login():
    # if already logged in, don't display login page
    if checkAuth():
        if dbfunctions.studentInit(c,session['username']):
            return redirect(url_for('studentInfo'))
        return redirect(url_for('welcome'))
    else:
        return render_template('login.html')

@app.route("/loginauth", methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    c.execute("SELECT hashpassword FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a == None: #checks login username and password
        flash("No user found with given username") #no given username in database
        return redirect(url_for('login'))
    elif password != a[0]:
        flash("Incorrect password") #password is incorrect for given username
        return redirect(url_for('login'))
    else: #successfully pass the tests
        session['username'] = username
        session['admin'] = dbfunctions.isAdmin(c, username)
        flash("Welcome " + username + ". You have been logged in successfully.")
        if isAdmin():
            flash("You are logged in as admin.")
            return redirect(url_for('adminHome'))
        # if student has been initialized, go directly to welcome page
        if dbfunctions.studentInit(c, username):
            return redirect(url_for('studentHome'))
        else: #initialize student w basic data
            return redirect(url_for('studentInfo'))

@app.route("/studentHome")
def studentHome():
    if checkAuth():
        return render_template('stu_home.html')
    return redirect(url_for('root'))

@app.route("/myOps")
def myOps():
    if checkAuth():
        # collection = relOps(session['username'])
        collection = dbfunctions.getAllOps(c)
        # the problem is that this only returns the ids of oeach of the ops
        return render_template('myOps.html')
    return redirect(url_for('root'))

@app.route("/allOps")
def allOps():
    if checkAuth():
        collection = dbfunctions.getAllOps(c)
        print(collection)
        return render_template('allOps.html', op_list = collection, admin=isAdmin())
    return redirect(url_for('root'))

#loads page to view opportunity details
@app.route("/<opid>")
def view_op(opid):
    if checkAuth():
        name = get("opportunities", "name", "WHERE opid = '%s'" % opid)[0][0]
        ## need interests and grades
        description = get("opportunities", "title", "WHERE opid = '%s'" % opid)[0][0]
        link = get("opportunities", "link", "WHERE opid = '%s'" % opid)[0][0]
        cost = get("opportunities", "cost", "WHERE opid = '%s'" % opid)[0][0]
        location = get("opportunities", "location", "WHERE opid = '%s'" % opid)[0][0]
        due_date = get("opportunities", "due_date", "WHERE opid = '%s'" % opid)[0][0]
        posted = get("opportunities", "posted", "WHERE opid = '%s'" % opid)[0][0]
        start_date = get("opportunities", "start_date", "WHERE opid = '%s'" % opid)[0][0]
        end_date = get("opportunities", "end_date", "WHERE opid = '%s'" % opid)[0][0]
        notes = get("opportunities", "notes", "WHERE opid = '%s'" % opid)[0][0]
        return render_template(
            "view_op.html",
            name = name,
            description = description,
            link = link,
            cost = cost,
            location = location,
            due_date = due_date,
            posted = posted,
            start_date = start_date,
            end_date = end_date,
            notes = notes
        )

@app.route('/adminHome')
def adminHome():
    if checkAuth() and isAdmin():
        return render_template('adm_home.html')
    return redirect(url_for('studentHome'))

@app.route("/addOp")
def addOp():
    if checkAuth() and isAdmin():
        return render_template('add_op.html')
    return redirect(url_for('studentHome'))

@app.route("/addOpAuth", methods=["POST"])
def addOpAuth():
    print(request.form)
    print(request.form['ints'])
    # ints_string=""
    ints = request.form.getlist("ints") #list of interests
    grades = request.form.getlist("grades")
    #get 9,10,11,12 into booleans
    n=False
    te=False
    e=False
    tw=False
    for grade in grades:
        if grade=="9":
            print(9)
            n = True
        if grade=="10":
            print(10)
            te = True
        if grade=="11":
            print(11)
            e = True
        if grade=="12":
            print(12)
            tw=True
    if "edit-op-button" in request.form.keys():
        print(request.form)
        id = request.form["opid"]
        dbfunctions.editOp(c, id, request.form['name'], request.form['des'], n, te, e, tw)
    else:
        id = dbfunctions.createOp(c, request.form['name'], request.form['des'], n, te, e, tw)
    print(id)
    #add interests individually
    for int in ints:
        dbfunctions.addInterest(c, id, int)
    # add other optional fields to Opportunity
    for key in request.form:
        print(key)
        if "op-button" not in key and key != "ints" and key != "grades" and key != "name" and key != "des" and request.form[key]:
            dbfunctions.updateOp(c, id, key, request.form[key])
    #add date posted (today) to opportunity info
    dbfunctions.updateOp(c, id, "posted", datetime.today().strftime('%Y-%m-%d'))
    db.commit()
    return redirect(url_for('adminHome'))

@app.route("/editOpp/<id>")
def editOpp(id):
    cur = dbfunctions.getOp(c, id)
    return render_template("edit_op.html", op=cur, opid=id)

@app.route("/logout")
def logout():
    session.pop("username")
    session.pop('admin')
    return redirect(url_for('root'))

@app.route("/adminCalendar")
def showCalendar():
    return render_template("adminCalendar.html")

@app.route("/addEvent")
def event():
    return render_template("addEvent.html")

@app.route("/adminEvent")
def addEvent():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    TIMEZONE = 'America/New_York'
    EVENT = {
        'summary': request.args["input"],
        'start'  : {'dateTime': request.args["startDate"] + "T" + request.args["startTime"],
                    'timeZone': TIMEZONE},
        'end'    : {'dateTime': request.args["endDate"] + "T" + request.args["endTime"],
                    'timeZone': TIMEZONE},
    }
    service.events().insert(calendarId = 'primary', body = EVENT).execute()
    return render_template("adminCalendar.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
