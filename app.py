from flask import Flask, render_template, redirect, url_for, session, flash, request
from urllib.request import urlopen
import json
import sqlite3, os, requests

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "HumanJello.db"

# open if file exists, otherwise create
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()  # facilitate db operations


@app.route('/admin/<username>')
def admin(username):
    c.execute('SELECT * FROM opportunities')
    return render_template('admin.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
