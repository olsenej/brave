#!/usr/bin/python3

# row[0]: name
# row[1]: portrait
# row[2]: q
# row[3]: w
# row[4]: e
# row[5]: r
# row[6]: passive

import json
import pprint
import os.path
import os
import pymysql.cursors

from __main__ import *
conn=pymysql.connect(host='localhost', user='ec2-user', passwd='m4ris4', db='bravery')

portrait_path = 'images/portraits/'
skill_path = 'images/skills/'
passive_path = 'images/passives/'

with conn.cursor() as cursor:
	for i in champs:
		champ_id = response_champs['data'][i]['id']
		champ_name = response_champs['data'][i]['name']
		portrait = portrait_path+i+'.png'
		q_skill = response_champs['data'][i]['spells'][0]['image']['full']
		w_skill = response_champs['data'][i]['spells'][1]['image']['full']
		e_skill = response_champs['data'][i]['spells'][2]['image']['full']
		r_skill = response_champs['data'][i]['spells'][3]['image']['full']
		passive_icon = response_champs['data'][i]['passive']['image']['full']
	
		sql = "INSERT IGNORE INTO champions (id, name, portrait, q, w, e, r, passive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
		cursor.execute(sql, (champ_id,i, portrait, skill_path+q_skill, skill_path+w_skill, skill_path+e_skill, skill_path+r_skill, passive_path+passive_icon))
		conn.commit()
		#print('Name: '+i+'|Portrait: '+portrait_path+portrait+'|Q: '+skill_path+q_skill+'|W: '+skill_path+w_skill+'|E: '+skill_path+e_skill+'|R: '+skill_path+r_skill+'|Passive path: '+passive_path+passive_icon)

conn.close()

