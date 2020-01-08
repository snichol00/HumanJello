from flask import Flask, render_template, redirect, url_for, session, flash, request
import json
import sqlite3, os, requests
from utl import dbfunctions

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "HumanJello.db"
#setup databases:
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations
dbfunctions.setup()


@app.route("/")
def root():
    return render_template("root.html")

@app.route("/studentAccount")
def studacc():
    return render_template("register.html", student=True);

@app.route("/register", methods=["POST"])
def registerstudent():
    if request.method == "POST":
        #determine if person registering was student or admin
        if 'adminCode' in request.form:
            admin = True
            register_route = 'registerAdmin'
        else:
            student = True
            register_route = 'registerStudent'
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        c.execute("SELECT username FROM users WHERE username = ?", (username, ))
        a = c.fetchone()
        if a != None: #checks for duplicate usernames
            flash("Account with that username already exists")
            return redirect(url_for(register_route))
        elif " " in username: #checks for spaces cause spaces suck
            flash("Username cannot contain spaces")
            return redirect(url_for(register_route))
        elif password != password2: #checks if both passwords are the same
            flash("Passwords do not match")
            return redirect(url_for(register_route))
        elif len(password) < 8: #passwords must have a minimum length of 8
            flash("Password must be at least 8 characters in length")
            return redirect(url_for(register_route))

        else: #successfully created an account
            if student:
                #dbfunctions.addStudent(username, password, )
            #dbfunctions.newUserTable(c, username)
            db.commit()
            flash("Successfuly created user")
            return redirect(url_for('studentLogin'))
    else:
        flash("GET request")
        return redirect(url_for('registerStudent'))


if __name__ == "__main__":
    app.debug = True;
    app.run()
