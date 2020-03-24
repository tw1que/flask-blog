'''
Create a SQLite3 table and populate it with mock data
'''

import sqlite3

# Create a new database if it does not already exist
with sqlite3.connect('blog.db') as connection:

	# Create a cursor object to execute SQL commands
	cursor = connection.cursor()

	# Create the table
	cursor.execute("CREATE TABLE IF NOT EXISTS posts (title TEXT, post TEXT)")

	# Insert mock data into table
	mock_posts = [
				('Good', 'I\'m good'),
				('Well', 'I\'m well'),
				('Excellent', 'I\'m excellent'),
				('Okay', 'I\'m okay')
				]

	cursor.executemany("INSERT INTO posts (title, post) VALUES (?, ?)", mock_posts)