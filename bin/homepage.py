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
	id_array = []
	for i in range(cursor.rowcount):
		row = cursor.fetchone()
		id_array.append(row[0])
		#homepage.write('<img src=\"'+row[2]+'\"><img src=\"'+row[3]+'\"><img src=\"'+row[4]+'\"><img src=\"'+row[5]+'\"><img src=\"'+row[6]+'\"><br/>')

	sql = "SELECT * FROM champions WHERE id=%s;"
	rando = randint(0,len(id_array))
	cursor.execute(sql, (id_array[rando]))
	rand_champ = cursor.fetchone()
	champ = rand_champ[2]

	rando = randint(0,len(id_array))
	cursor.execute(sql, (id_array[rando]))
	rand_champ = cursor.fetchone()
	q = rand_champ[3]

	rando = randint(0,len(id_array))
	cursor.execute(sql, (id_array[rando]))
	rand_champ = cursor.fetchone()
	w = rand_champ[4]

	rando = randint(0,len(id_array))
	cursor.execute(sql, (id_array[rando]))
	rand_champ = cursor.fetchone()
	e = rand_champ[5]

	rando = randint(0,len(id_array))
	cursor.execute(sql, (id_array[rando]))
	rand_champ = cursor.fetchone()
	r = rand_champ[6]

	homepage.write('<img src=\"'+champ+'\"><img src=\"'+q+'\"><img src=\"'+w+'\"><img src=\"'+e+'\"><img src=\"'+r+'\"><br/>')

cursor.close()
conn.close()
homepage.close()
