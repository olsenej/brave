#!/usr/bin/python3

import json
import pprint
import os.path
import os
import pymysql.cursors

#from __main__ import *
from webscrape import response_champs
from webscrape import champs
from webscrape import response_items
from webscrape import items
from webscrape import response_summoners
from webscrape import summoners
from webscrape import maps

conn=pymysql.connect(host='localhost', user='ec2-user', passwd='pdcd', db='bravery')

portrait_path = 'images/portraits/'
skill_path = 'images/skills/'
passive_path = 'images/passives/'
item_path = 'images/items/'
summoner_path = 'images/summoners/'
try:
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
		for i in items:
	# id | name | gold | crystal_scar | twisted_treeline | summoners_rift | howling_abyss | icon 
			item_id = response_items['data'][i]['id']
			item_name = response_items['data'][i]['name']
			item_gold = response_items['data'][i]['gold']['total']
			item_icon = response_items['data'][i]['image']['full']
			item_map_cs = False
			item_map_tt = True
			item_map_sr = True
			item_map_ha = True
			counter = 0
			for map_number in maps:
				for counter in range(len(maps[map_number]['unpurchasableItemList'])):
					if item_id == maps[map_number]['unpurchasableItemList'][counter]:
						if map_number == '10':
							item_map_tt = False
						elif map_number == '11':
							item_map_sr = False
						elif map_number == '12':
							item_map_ha = False

			sql = "INSERT IGNORE INTO items (id, name , gold, crystal_scar, twisted_treeline, summoners_rift, howling_abyss, icon) VALUES (%r, %s, %r, %r, %r, %r, %r, %s);"
			cursor.execute(sql, (item_id, item_name, item_gold, item_map_cs, item_map_tt, item_map_sr, item_map_ha, item_path+item_icon))
			conn.commit()

		for i in summoners:
			summoner_id = response_summoners['data'][i]['id']
			summoner_name = response_summoners['data'][i]['name']
			summoner_icon = response_summoners['data'][i]['image']['full']
			summoner_map_cs = False
			summoner_map_tt = False
			summoner_map_sr = False
			summoner_map_ha = False
			counter = 0
			for mode in response_summoners['data'][i]['modes']:
				if mode == 'CLASSIC':
					summoner_map_tt = True
					summoner_map_sr = True
				elif mode == 'ARAM':
					summoner_map_ha = True
				elif mode == 'ODIN':
					summoner_map_cs = True
			sql = "INSERT IGNORE INTO summoners (id, name, crystal_scar, twisted_treeline, summoners_rift, howling_abyss, icon) VALUES (%s, %s, %r, %r, %r, %r, %s);"
			cursor.execute(sql, (summoner_id, summoner_name, summoner_map_cs, summoner_map_tt, summoner_map_sr, summoner_map_ha, summoner_path+summoner_icon))
			conn.commit()
			#print(str(summoner_id) +" "+ summoner_name+" "+str(summoner_map_cs)+" "+ str(summoner_map_tt)+" "+ str(summoner_map_sr)+" "+ str(summoner_map_ha)+" "+ summoner_path+summoner_icon)
finally:
	conn.close()

