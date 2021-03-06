#!/usr/bin/python3
from random import randint
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from flask_bootstrap import Bootstrap
import pymysql
import re

# create our little application :)
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.debug=True


def connect_db():
	return pymysql.connect(host='localhost', user='ec2-user', passwd='pdcd', db='bravery')

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def roll_items(summoners = []):
	### Generate item id array omitting basic items and Viktor's Hex Core
	cur = g.db.cursor()
	item_id_array = []
	boot_id_array = []
	final_build = []
	smite  = 'images/summoners/SummonerSmite.png'
	jungle_param = '"Enchantment%"'
	jungle_item = False
	jamble = re.compile("^Enchantment.*$")
	cur.execute("SELECT * FROM items WHERE howling_abyss=1 AND gold>=2000 AND (id != 3200 AND id != 3198 AND id != 3197 AND id != 3196) AND name not like 'Eye of the%';")
	for i in range(cur.rowcount):
		row = cur.fetchone()
		item_id_array.append(row[0])
	
	### Add Tier 3 Boots to build first
	cur.execute("SELECT * FROM items WHERE howling_abyss=1 AND (name LIKE '%Alacrity%' OR name LIKE '%Captain%' OR name LIKE '%Furor%' OR name LIKE '%Distortion%' OR name LIKE '%Homeguard%') AND (id !=3240 AND id != 3241 AND id !=3242 AND id !=3243 AND id !=3244 AND id !=3245);")
	for i in range(cur.rowcount):
		row = cur.fetchone()
		boot_id_array.append(row[0])
	rando = randint(0,len(boot_id_array)-1)
	sql = "SELECT * FROM items WHERE howling_abyss=1 AND id=%s"
	cur.execute(sql, (boot_id_array[rando]))
	final_build.append([dict(name=row[1], icon=row[7]) for row in cur.fetchall()])
	
	### Add the rest of the items to build
	while len(final_build) < 6:
		rando = randint(0,len(item_id_array)-1)
		sql = "SELECT * FROM items WHERE id=%s;"
		cur.execute(sql, (item_id_array[rando]))
		check = cur.fetchone()
		### Check if rolled a jungle item
		if jamble.match(check[1]): ### Aparently too stupid to use any() but regex is ok
			### Found a jungle item
			if smite in summoners[0][0] or smite in summoners[1][0]:
				if jungle_item == True:
					sql = "SELECT * from items WHERE id=%s AND name NOT LIKE %s;"
					rando = randint(0,len(item_id_array)-1)
					cur.execute(sql, (item_id_array[rando], jungle_param))
					### Already have a jungle item
				elif jungle_item == False:
					sql = "SELECT * FROM items WHERE id=%s;"
					cur.execute(sql, (item_id_array[rando]))
					jungle_item = True
					### First jungle item
					final_build.append([dict(name=row[1], icon=row[7]) for row in cur.fetchall()])
		else:
			sql = "SELECT * FROM items WHERE id=%s;"
			cur.execute(sql, (item_id_array[rando]))
			### Not a jungle item
			final_build.append([dict(name=row[1], icon=row[7]) for row in cur.fetchall()])
	return final_build

def roll_summoners():
	cur = g.db.cursor()
	summoners = []
	used_summoners = []
	cur.execute("SELECT * FROM summoners WHERE howling_abyss=1;")
	summoner_id_array = []
	for i in range(cur.rowcount):
		row = cur.fetchone()
		summoner_id_array.append(row[0])
	#for i in range(0,2):
	while len(summoners) < 2:
		rando = randint(0,len(summoner_id_array)-1)
		sql = "SELECT * FROM summoners WHERE id=%s"
		cur.execute(sql, (summoner_id_array[rando]))
		if rando in used_summoners:
			while True:
				if rando in used_summoners:
					rando = randint(0,len(summoner_id_array)-1)
					cur.execute(sql, (summoner_id_array[rando]))
				else:
					summoners.append([dict(name=row[1], icon=row[6]) for row in cur.fetchall()])
					used_summoners.append(rando)
					break
		summoners.append([dict(name=row[1], icon=row[6]) for row in cur.fetchall()])
		used_summoners.append(rando)
	if len(summoners) > 2:
		summoners.pop()
	return summoners

def roll_champ():
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
	skill_button = [i[0] for i in cur.description]
	champ = [dict(name=row[1], portrait=row[2], skill_icon=row[rando], skill_name=skill_button[rando], skin_number=randint(0,int(row[8]))) for row in cur.fetchall()]
	return champ

def roll_masteries():
		of_pts = randint(0,18)

		temp = 30-of_pts
		if temp > 18:
			temp = 18
		ut_pts=randint(0,temp)

		df_pts=30-(of_pts+ut_pts)
		if df_pts > 18:
			df_pts = 18
		if of_pts+df_pts+ut_pts < 30:
			while (of_pts+df_pts+ut_pts) < 30:
				if (randint(1,2)%2) == 0 and of_pts <18:
					of_pts+=1
				elif (randint(1,2)%2) == 1 and df_pts<18:
					df_pts+=1
		masteries = [dict(offense=of_pts, defense=df_pts, utility=ut_pts)]
		return masteries

@app.route('/')
def index():
	### Roll champion and ability
	champ = roll_champ()
	
	### Roll summoners
	summoners = roll_summoners()

	### Roll Items
	final_build = roll_items(summoners)

	### Roll Masteries
	masteries = roll_masteries()

#	if .validate_on_submit():
#		if 'aram' in request.form:
#			pass  
#		elif 'tree' in request.form:
#			pass


	response = make_response(render_template('index.html', champ=champ, summoners=summoners, final_build=final_build, masteries=masteries))
	response.set_cookie('map','aram')
	return response


@app.route('/images')
def render_image(image_path):
	image_path='/images/'
	return send_from_directory('',image_path)  

@app.route('/js')
def render_node(node_path):
	node_path='/node_modules/zeroclipboard/dist/'
	return send_from_directory('',node_path)

if __name__ == '__main__':
    app.run()

