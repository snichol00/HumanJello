from flask import Flask, render_template, redirect, url_for, session, flash, request
import json, sys
import sqlite3, os
import dbfunctions

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "HumanJello.db"

"""Setup databases"""
# open if file exists, otherwise create
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()  # facilitate db operations
dbfunctions.setup()


@app.route("/")
def root():
    return render_template("root.html")

def checkAuth(): #checks if the user is logged in
    if "userID" in session:
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
            student = True
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

        else:  # successfully created an account
            c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
            dbfunctions.newUserTable(c, username)
            if student:
                dbfunctions.createStudent(c, username, password)
                db.commit()
                return redirect(url_for('login'))
            #dbfunctions.newUserTable(c, username)
            db.commit()
            flash("Successfuly created user")
            return redirect(url_for('studentLogin'))
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
        # if student has been initialized, go directly to welcome page
        if dbfunctions.studentInit(c, username):
            return redirect(url_for('welcome'))
        else: #initialize student w basic data
            return redirect(url_for('studentInfo'))

@app.route("/studentHome")
def studentHome():
    if checkAuth():
        return render_template('stu_home.html')
    return redirect(url_for('root'))

@app.route('/admin/<username>')
def admin(username):
    c.execute('SELECT * FROM opportunities')
    return render_template('admin.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
