from flask import Flask, g, render_template, request, abort
import sqlite3
import numpy as np


# -- leave these lines intact --
app = Flask(__name__)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker.db')
        g.sqlite_db = sqlite3.connect(db_name)

    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()
# ------------------------------


@app.route('/',methods=['GET','POST'])
def root():
    conn = get_db()
    c = conn.cursor()
    names = ["xixi","hehe"]
    if request.method == "POST":
        key = request.form.get("className")
        member = (["Swimming","Ballet","Climbing"])
        member.append(key)
        common = []
        wholeClass = []
        names = ""
        c.execute("SELECT class FROM posts")
        eachclass = list(c.fetchall())
        print len(eachclass)
        for i in range(len(eachclass)):
            each = ''.join(eachclass[i])
            classEach = [x.strip() for x in each.split(',')]
            wholeClass.append(classEach)
        for i in range(len(wholeClass)):
            a = np.intersect1d(member,wholeClass[i])
            common.append(len(a))
        commonC = np.array(common)
        sort = commonC.argsort()[-3:][::-1]
        c.execute("SELECT name FROM posts WHERE id=?",[sort[0]])          
        names = c.fetchall()
        return render_template("result.html",content = names )
    else:
        return render_template("home.html")
if __name__ == '__main__':
    app.run()
