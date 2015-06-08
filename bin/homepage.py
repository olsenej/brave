#!/usr/bin/python3
# row[0]: id
# row[1]: name
# row[2]: portrait
# row[3]: q
# row[4]: w
# row[5]: e
# row[6]: r
# row[7]: passive

import json
import pprint
import os.path
import os
import pymysql.cursors
from random import randint
from flask import Flask

conn=pymysql.connect(host='localhost', user='ec2-user', passwd='m4ris4', db='bravery')
homepage = open('../index.html', 'w')

with conn.cursor() as cursor:
	cursor.execute("SELECT * FROM champions")
	champ_id_array = []
	for i in range(cursor.rowcount):
		row = cursor.fetchone()
		champ_id_array.append(row[0])

	sql = "SELECT * FROM champions WHERE id=%s;"
	rando = randint(0,len(champ_id_array))
	cursor.execute(sql, (champ_id_array[rando]))
	rand_champ = cursor.fetchone()
	champ = rand_champ[2]

	cursor.execute("SELECT * FROM items")
	item_id_array = []
	for i in range(cursor.rowcount):
                row = cursor.fetchone()
                item_id_array.append(row[0])

	sql = "SELECT icon FROM items WHERE id=%s;"
	rando = randint(0,len(item_id_array))
	cursor.execute(sql, (item_id_array[rando]))
	rand_item = cursor.fetchone()
	item1 = rand_item

	rando = randint(0,len(item_id_array))
	cursor.execute(sql, (item_id_array[rando]))
	rand_item = cursor.fetchone()
	item2 = rand_item

	rando = randint(0,len(item_id_array))
	cursor.execute(sql, (item_id_array[rando]))
	rand_item = cursor.fetchone()
	item3 = rand_item

	rando = randint(0,len(item_id_array))
	cursor.execute(sql, (item_id_array[rando]))
	rand_item = cursor.fetchone()
	item4 = rand_item

	rando = randint(0,len(item_id_array))
	cursor.execute(sql, (item_id_array[rando]))
	rand_item = cursor.fetchone()
	item5 = rand_item

	rando = randint(0,len(item_id_array))
	cursor.execute(sql, (item_id_array[rando]))
	rand_item = cursor.fetchone()
	item6 = rand_item


	homepage.write('<img src=\"'+champ+'\"><img src=\"'+item1[0]+'\"><img src=\"'+item2[0]+'\"><img src=\"'+item3[0]+'\"><img src=\"'+item4[0]+'\"><img src=\"'+item5[0]+'\"><img src=\"'+item6[0]+'\"><br/>')

cursor.close()
conn.close()
homepage.close()
