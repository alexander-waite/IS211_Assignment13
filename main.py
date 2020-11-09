from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)
newlist = []


@app.route('/')
def hello_world():
    author = "beast mode beast mode"
    name = "apex predator"
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
