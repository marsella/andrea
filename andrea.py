import init
from init import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = [dict(idnum=row[0], title=row[1], text=row[2], category=row[3]) 
             for row in cur.fetchall()]
  return (rv[0] if rv else None) if one else rv 

@app.route('/')
def show_entries():
  entries = query_db('select id, title, text, category from entries \
                       order by id desc ')
    
  return render_template('show_entries.html', entries=entries)

@app.route('/category/<string:category>')
def show_category(category):
  entries = query_db('select id, title, text, category from entries where \
                 category = ? order by id desc ', [category])
  return render_template('show_entries.html', entries=entries)

@app.route('/add_form')
def add_entry_form():
  if not session.get('logged_in'):
    abort(401)
  return render_template('add_entry.html')

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  query_db('insert into entries (title, text, category) values \
           (?, ?, ?)', [request.form['title'], request.form['text'],
           request.form['category']])
  query_db('insert into categories (cat) values (?)',
           [request.form['category']])
  g.db.commit()
  flash('New entry was successfully posted')
  return redirect(url_for('show_entries'))

@app.route('/remove/<int:idnum>')
def remove_entry(idnum):
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('DELETE from entries WHERE id = ?', [idnum])
  g.db.commit()
  flash('Entry successfully deleted')
  return redirect(url_for('show_entries'))

@app.route('/commission')
def commission():
  return render_template('commission.html')

@app.route('/sendmail')
def send_mail():
  flash('DIDN\'T ACTUALLY SEND THAT!!!')
  return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('Success! Logged in.')
      return redirect(url_for('show_entries'))
  return render_template('login.html', error=error)


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('Success! Logged out.')
  return redirect(url_for('show_entries'))

if __name__ == '__main__':
  app.run()

