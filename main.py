from flask import Flask, render_template, request, redirect
import logging
from logging import FileHandler
import os


app = Flask(__name__)
newlist = []


def logfile_start():
    file_handler = FileHandler(os.getcwd()+"/log.txt")
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


def sql_load_sample():
    import sqlite3 as lite

    def db_setup(query_str=str()):
        conn = lite.connect('pet.db')
        c = conn.cursor()
        for l in query_str:
            c.execute(l)
            conn.commit()
        conn.close()

    def split_query(query_str=str(), split=str()):
        query_split = query_str.split(split)
        query_return = []
        for l in query_split:
            l = "INSERT INTO " + l.strip()
            l = l.replace(':', ' VALUES')

            query_return = query_return + [l.strip()]
        query_return.pop()
        return query_return

    query = """Person: (1, 'James', 'Smith', 41)
             Person: (2, 'Diana', 'Greene', 23)
             Person: (3, 'Sara', 'White', 27)
             Person: (4, 'William', 'Gibson', 23)
             Pet: (1, 'Rusty', 'Dalmation', 4, 1)
             Pet: (2, 'Bella', 'Alaskan Malamute', 3, 0)
             Pet: (3, 'Max', 'Cocker Spaniel', 1, 0)
             Pet: (4, 'Rocky', 'Beagle', 7, 0)
             Pet: (5, 'Rufus', 'Cocker Spaniel', 1, 0)
             Pet: (6, 'Spot', 'Bloodhound', 2, 1)
             Person_Pet: (1, 1)
             Person_Pet: (1, 2)
             Person_Pet: (2, 3)
             Person_Pet: (2, 4)
             Person_Pet: (3, 5)
             Person_Pet: (4, 6)"""

    query = split_query(query, '\n')
    for line in query:
        print(line)
    db_setup(query)


@app.route('/')
def hello_world():
    logfile_start()
    author = "author"
    name = "name"
    return render_template('index.html', author=author, name=name, fakelist=newlist)


@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    def check_items(task, email, priority):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            if priority in ['low', 'medium', 'high']:
                newlist.append([task, email, priority])
        else:
            pass
        return redirect('/')

    check_items(task, email, priority)
    return redirect('/')


@app.route('/clear', methods=['POST'])
def clear():
    newlist.clear()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)

# export FLASK_APP=hello.py
# flask run
# https://realpython.com/the-model-view-controller-mvc-paradigm-summarized-with-legos/
# http: // opentechschool.github.io / python - flask / core / files - templates.html
