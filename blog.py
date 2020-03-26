# blog.py - controller

from flask import Flask, render_template, request, session, \
	flash, redirect, url_for, g
from functools import wraps
import sqlite3

# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = r'\xdb\xfb=H3\x00\xff\xac\xccc\x93\xfd\x8b\xbbk;n\xa0\x7fb\x92\x97>\xa5!N\x18\x97^\x95\x0b\xbc'

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function for connecting to the database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(func):

	@wraps(func)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return func(*args, **kwargs)
		else:
			flash('You need to log in first')
			return redirect(url_for('login'))

	return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	status_code = 200
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or \
				request.form['password'] != app.config['PASSWORD']:
				error = 'Invalid Credentials. Please try again.'
				status_code = 401

		else:
			session['logged_in'] = True
			return redirect(url_for('main'))

	return render_template('login.html', error=error), status_code

@app.route('/main')
@login_required
def main():
	with connect_db() as g.db:
		cur = g.db.execute("SELECT * FROM posts")
		posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]

	return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']

	if not title or not post:
		flash('All fields are required. Please try again')
		return redirect(url_for('main'))

	else:
		with connect_db() as g.db:
			g.db.execute("INSERT INTO posts (title, post) VALUES (?,?)", 
				[request.form['title'], request.form['post']])
		flash('New entry was succesfully posted!')
		return redirect(url_for('main'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You where logged out')
	return redirect(url_for('login'))


if __name__=='__main__':
	app.run(debug=True)

