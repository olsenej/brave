#!/usr/bin/python3
from random import randint
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import pymysql
import re

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

def roll_items():
	### Generate item id array omitting basic items and Viktor's Hex Core
	cur = g.db.cursor()
	item_id_array = []
	boot_id_array = []
	final_build = []
	jungle_param = "Enchantment%"
	jungle_item = False
	jamble = re.compile("^Enchantment.*$")
	cur.execute("SELECT * FROM items WHERE twisted_treeline=1 AND gold>=2000 AND (id != 3200 OR id != 3198 OR id != 3197 OR id != 3196);")
	for i in range(cur.rowcount):
		row = cur.fetchone()
		item_id_array.append(row[0])
	
	### Add Tier 3 Boots to build first
	cur.execute("SELECT * FROM items WHERE twisted_treeline=1 AND (name LIKE '%Alacrity%' OR name LIKE '%Captain%' OR name LIKE '%Furor%' OR name LIKE '%Distortion%' OR name LIKE '%Homeguard%');")
	for i in range(cur.rowcount):
		row = cur.fetchone()
		boot_id_array.append(row[0])
	rando = randint(0,len(boot_id_array)-1)
	sql = "SELECT * FROM items WHERE twisted_treeline=1 AND id=%s"
	cur.execute(sql, (boot_id_array[rando]))
	final_build.append([row[7] for row in cur.fetchall()])
	
	### Add the rest of the items to build
	for i in range(1,6):
		rando = randint(0,len(item_id_array)-1)
		if jungle_item == True:
			sql = "SELECT * from items WHERE id=%s AND name NOT LIKE %s;"
			cur.execute(sql, (item_id_array[rando], jungle_param))
		elif jungle_item == False:
			sql = "SELECT * FROM items WHERE id=%s;"
			cur.execute(sql, (item_id_array[rando]))

		check = cur.fetchone()
		#print(check[1])
		if jamble.match(check[1]): ### Aparently too stupid to use any() but regex is ok
			if jungle_item == False:
				jungle_item = True
			elif jungle_item == True:
				### Reroll until no jungle
				jungle_item == True
			sql = "SELECT * from items WHERE id=%s AND name NOT LIKE %s;"
			cur.execute(sql, (item_id_array[rando], jungle_param))
		sql = "SELECT * FROM items WHERE id=%s;"
		cur.execute(sql, (item_id_array[rando]))
		final_build.append([row[7] for row in cur.fetchall()])

	return final_build

@app.route('/')
def index():
	### Roll Champion
	cur = g.db.cursor()
	cur.execute("SELECT * FROM champions;")
	champ_id_array = []
	for i in range(cur.rowcount):
		row = cur.fetchone()
		champ_id_array.append(row[0])

	rando = randint(0,len(champ_id_array)-1)
	sql = "SELECT * FROM champions WHERE id=%s;"
	cur.execute(sql, (champ_id_array[rando]))

	rando = randint(3,5)
	entries = [dict(name=row[1], portrait=row[2], max_skill=row[rando],  passive=row[7]) for row in cur.fetchall()]

	### Roll Masteries
	rando = randint(0,30)
	of_pts = rando
	rando = randint(0,30-of_pts)
	df_pts=rando
	ut_pts=30-(of_pts+df_pts)
	masteries = [dict(offense=of_pts, defense=df_pts, utility=ut_pts)]

	### Roll Items
	final_build=roll_items()

	return render_template('index.html', entries=entries, final_build=final_build, masteries=masteries)


@app.route('/images')
def render_image(image_path):
	image_path='/images/'
	return send_from_directory('',image_path)  



if __name__ == '__main__':
    app.run()

