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
	jungle_param = '"Enchantment%"'
	jungle_item = False
	jamble = re.compile("^Enchantment.*$")
	cur.execute("SELECT * FROM items WHERE twisted_treeline=1 AND gold>=2000 AND (id != 3200 AND id != 3198 AND id != 3197 AND id != 3196);")
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
		print("Loop start"+ str(jungle_item))
		rando = randint(0,len(item_id_array)-1)
		sql = "SELECT * FROM items WHERE id=%s;"
		cur.execute(sql, (item_id_array[rando]))
		check = cur.fetchone()
		### Check if rolled a jungle item
		if jamble.match(check[1]): ### Aparently too stupid to use any() but regex is ok
			### Found a jungle item
			if jungle_item == True:
				sql = "SELECT * from items WHERE id=%s AND name NOT LIKE %s;"
				rando = randint(0,len(item_id_array)-1)
				cur.execute(sql, (item_id_array[rando], jungle_param))
				### Already have a jungle item
				print("Already have" + str(jungle_item))
			elif jungle_item == False:
				sql = "SELECT * FROM items WHERE id=%s;"
				cur.execute(sql, (item_id_array[rando]))
				jungle_item = True
				### First jungle item
				print("First jungle"+ str(jungle_item))
		else:
			sql = "SELECT * FROM items WHERE id=%s;"
			cur.execute(sql, (item_id_array[rando]))
			### Not a jungle item
			print("Not a jungle"+ str(jungle_item))

		### Add item
		print("Add item"+ str(jungle_item))
		final_build.append([row[7] for row in cur.fetchall()])

	return final_build

def roll_summoners():
	cur = g.db.cursor()
	summoners = []
	cur.execute("SELECT * FROM summoners WHERE twisted_treeline=1;")
	summoner_id_array = []
	for i in range(cur.rowcount):
		row = cur.fetchone()
		summoner_id_array.append(row[0])
	for i in range(0,2):
		rando = randint(0,len(summoner_id_array)-1)
		sql = "SELECT * FROM summoners WHERE id=%s"
		cur.execute(sql, (summoner_id_array[rando]))
		summoners.append([row[6] for row in cur.fetchall()])
	return summoners

@app.route('/')
def index():
	### Roll Champion and skill
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
	entries = [dict(name=row[1], portrait=row[2], max_skill=row[rando]) for row in cur.fetchall()]
	
	### Roll summoners
	summoners = roll_summoners()

	### Roll Items
	final_build = roll_items()

	### Roll Masteries
	rando = randint(0,30)
	of_pts = rando
	rando = randint(0,30-of_pts)
	df_pts=rando
	ut_pts=30-(of_pts+df_pts)
	masteries = [dict(offense=of_pts, defense=df_pts, utility=ut_pts)]


	return render_template('index.html', entries=entries, summoners=summoners, final_build=final_build, masteries=masteries)


@app.route('/images')
def render_image(image_path):
	image_path='/images/'
	return send_from_directory('',image_path)  



if __name__ == '__main__':
    app.run()

