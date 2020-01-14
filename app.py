from flask import Flask, render_template, redirect, url_for, session, flash, request
import json, sys
import sqlite3, os
from utl import dbfunctions
import dbfunctions

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "HumanJello.db"
ADMIN_CODE = "admin"

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
    return redirect(url_for('welcome'))

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
            if !admin:
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
        # should run a function first to sorts Ops
        collection = get("opportunities", "opid, name")
        return render_template('myOps.html')
    return redirect(url_for('root'))

@app.route("/allOps")
def allOps():
    if checkAuth():
        collection = get("opportunities", "opid, name")
        return render_template('allOps.html')
    return redirect(url_for('root'))

@app.route('/adminHome')
def adminHome():
    return render_template('adm_home.html')

@app.route("/addOp")
def addOp():
    return render_template('add_op.html')

@app.route("/addOpAuth", methods=["POST"])
def addOpAuth():
    print(request.form)
    print(request.form['ints'])
    # ints_string=""
    for tuple in request.form:
        if tuple[0] == "ints":
            print(tuple[1])
    dbfunctions.createOp(c, request.form['name'], "ints_string", request.form['des'], "grades")
    return redirect(url_for('adminHome'))

@app.route("/logout")
def logout():
    session.pop['username']
    session.pop['admin']
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()
