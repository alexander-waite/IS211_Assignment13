from flask import Flask, render_template, request, redirect, url_for, g
import logging
from logging import FileHandler
import os
import sqlite3

app = Flask(__name__)
newlist = []


def logfile_start():
    file_handler = FileHandler(os.getcwd()+"/log.txt")
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)


@app.route('/')
def indexpage():
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from student")

    rows = cur.fetchall()
    return render_template("index2.html", rows=rows)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO student (student_id, student_first_name, student_last_name) VALUES (1,'John','Smith')")
    cur.execute("INSERT OR IGNORE INTO quizzes (quiz_id, quiz_subject, quiz_question_amount, quiz_date) VALUES (1, \
    'Python Basics', 5, 'February, 5th, 2015')")
    cur.execute("select student.student_id, student.student_first_name, student.student_last_name, \
                quizzes.quiz_id, quizzes.quiz_subject, quizzes.quiz_question_amount, quizzes.quiz_date \
                from student, quizzes")

    rows = cur.fetchall()
    con.close()
    return render_template("dashboard.html", rows=rows)



if __name__ == '__main__':
    app.run(debug=True)

# export FLASK_APP=hello.py
# flask run
# https://realpython.com/the-model-view-controller-mvc-paradigm-summarized-with-legos/
# http: // opentechschool.github.io / python - flask / core / files - templates.html
