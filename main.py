from flask import Flask, render_template, request, redirect, url_for, g
import logging
from logging import FileHandler
import os
import sqlite3
import datetime

app = Flask(__name__)
newlist = []


def logfile_start():
    file_handler = FileHandler(os.getcwd() + "/log.txt")
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
    cur.execute("select student.student_id, student.student_first_name, student.student_last_name from student")
    con.commit()
    rows = cur.fetchall()
    cur.execute(
        "select quizzes.quiz_id, quizzes.quiz_subject, quizzes.quiz_question_amount, quizzes.quiz_date from quizzes")
    con.commit()
    rows2 = cur.fetchall()
    con.close()
    return render_template("dashboard.html", rows=rows, rows2=rows2)


@app.route('/student/add', methods=['GET', 'POST'])
def add():
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT student_id FROM student WHERE student_id=(SELECT max(student_id) FROM student)")
    sid = [dict(id=row[0]) for row in cur.fetchall()][0]["id"] + 1
    con.close()
    if request.method == 'POST':
        if request.form['student_name'] is not None:
            try:
                student_name = request.form['student_name']
                student_name = student_name.split(' ')
                sfn, sln = '"' + student_name[0].strip() + '"', '"' + student_name[1].strip() + '"'
                con = sqlite3.connect('hw13.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                # TODO: insecure, fix if have time
                cur.execute(
                    "INSERT INTO student (student_id, student_first_name, student_last_name) VALUES ({}, {}, {})".format(
                        sid, sfn, sln))
                con.commit()
                con.close()
                return redirect('/dashboard')
            except:
                error = 'Invalid Name. Please try again.'
                return render_template('studentadd.html', error=error)
        else:
            return redirect(url_for('dashboard'))
    else:
        return render_template("studentadd.html")


@app.route('/quiz/add', methods=['GET', 'POST'])
def quizadd():
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("SELECT quiz_id FROM quizzes WHERE quiz_id=(SELECT max(quiz_id) FROM quizzes)")
        quiz_id = [dict(id=row[0]) for row in cur.fetchall()][0]["id"] + 1
    except(IndexError):
        quiz_id = 1
    con.close()
    if request.method == 'POST':
        if request.form['quiz_subject'] is not None:
            try:
                subject = '"' + request.form['quiz_subject'].strip() + '"'
                q_amt = request.form['quiz_question_amount'].strip()
                q_date = request.form['quiz_date'].strip()
                q_date = '"' + datetime.datetime.strptime(q_date, '%Y-%m-%d').strftime('%B %d,%Y') + '"'
                q_date = q_date
                print('quiz_id {}, subject {}, q_amt {} q_date {}'.format(quiz_id, subject, q_amt, q_date))
                con = sqlite3.connect('hw13.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                # TODO: insecure, fix if have time
                cur.execute(
                    "INSERT INTO quizzes (quiz_id, quiz_subject, quiz_question_amount, quiz_date) VALUES ({}, {}, {}, {})".format(
                        quiz_id, subject, q_amt, q_date))
                con.commit()
                con.close()
                return redirect('/dashboard')
            except:
                error = 'Invalid Name. Please try again.'
                return render_template('scoreadd.html', error=error)
        else:
            return redirect(url_for('dashboard'))
    else:
        return render_template("quizadd.html")


@app.route('/score/add', methods=['GET', 'POST'])
def scoreadd():
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("SELECT score_id FROM score WHERE score_id=(SELECT max(score_id) FROM score)")
        score_id = [dict(id=row[0]) for row in cur.fetchall()][0]["id"] + 1
    except(IndexError):
        score_id = 1

    cur.execute("SELECT student.student_id FROM student;")
    studentrows = cur.fetchall()

    cur.execute("SELECT quizzes.quiz_id FROM quizzes;")
    quizrows = cur.fetchall()

    con.close()

    if request.method == 'POST':
        if request.form['score_total'] is not None:
            try:
                student_id_input = request.form['student_id'].strip()
                quiz_id_input = request.form['quiz_id'].strip()
                score_total = request.form['score_total'].strip()
                print('student_id_input {}, quiz_id_input {}'.format(student_id_input, quiz_id_input))
                con = sqlite3.connect('hw13.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sql_secure_str = "INSERT INTO score(score_id, score_total, student_id, quiz_id) VALUES (?,?,?,?)"
                sql_secure_input = (score_id, score_total, student_id_input, quiz_id_input)
                cur.execute(sql_secure_str, sql_secure_input)
                con.commit()
                con.close()
                return redirect('/dashboard')
            except:
                error = 'Invalid Score Error. Please try again.'
                return render_template('scoreadd.html', error=error)
        else:
            return redirect(url_for('dashboard'))
    else:
        return render_template("scoreadd.html", quizrows=quizrows, studentrows=studentrows)


@app.route('/student/<int_sid>', methods=['GET', 'POST'])
def studentidpass(int_sid):
    error = 'Error, user not found'
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "SELECT score_id,score_total FROM score WHERE student_id= {}".format(int_sid))
    con.commit()
    rowscur = cur.fetchall()
    con.close()

    return render_template("studentsearch.html", rowscur=rowscur, error=error)


if __name__ == '__main__':
    app.run(debug=True)

# set FLASK_APP = main.py
# set FLASK_ENV=development
