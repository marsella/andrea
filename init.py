from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# config
DATABASE = '/tmp/andrea.db'
DEBUG = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
# both these lines?
app.config.from_object(__name__)
app.config.from_envvar('ANDREA_SETTINGS', silent=True)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  g.db.close()
