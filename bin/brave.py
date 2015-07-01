#!/usr/bin/python3
from random import randint
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import pymysql

# create our little application :)
app = Flask(__name__, static_folder = "")
app.config.from_object(__name__)
app.debug=True


def connect_db():
	return pymysql.connect(host='localhost', user='ec2-user', passwd='m4ris4', db='bravery')

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def index():
	cur = g.db.cursor()
	cur.execute("SELECT * FROM champions")
	champ_id_array = []
	for i in range(cur.rowcount):
		row = cur.fetchone()
		champ_id_array.append(row[0])

	rando = randint(0,len(champ_id_array))
	sql = "SELECT * FROM champions WHERE id=%s;"
	cur.execute(sql, (champ_id_array[rando]))
	rando = randint(3,5)
	
	entries = [dict(name=row[1], portrait=row[2], max_skill=row[rando],  passive=row[7]) for row in cur.fetchall()]

	return render_template('index.html', entries=entries)


@app.route('/images')
def render_image(image_path):
	image_path='/images/'
	return send_from_directory('',image_path)  



if __name__ == '__main__':
    app.run()

