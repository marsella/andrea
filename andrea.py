import init
from init import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

@app.route('/')
def show_entries():
  cur = g.db.execute('select id, title, text from entries order by id desc')
  entries = [dict(idnum=row[0], title=row[1], text=row[2]) 
             for row in cur.fetchall()]
  return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
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
