#!/usr/bin/python3
import urllib.request
import urllib.parse
import json
import pprint
import os.path

k = open('apikeyfile', 'r')
apikey = k.read()
k.close()

summoner_byname_url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/prisencolinensi?api_key=%s' % apikey
ddrag_realm_url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/realm?api_key=%s' % apikey
champ_byid_url = 'https://na.api.pvp.net/api/lol/na/v1.2/champion/1?api_key=%s' % apikey
champ_list_url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=passive,spells&api_key=%s' % apikey
item_list_url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/item?itemListData=gold,image&api_key=%s' % apikey
map_data_url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/map?api_key=%s' % apikey
summoner_list_url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell?spellData=image,modes&api_key=%s' % apikey

image_base_path = '../images/'
champ_square_path = image_base_path+'portraits/'
skill_path = image_base_path+'skills/'
item_path = image_base_path+'items/'
passive_path = image_base_path+'passives/'
summoner_path = image_base_path+'summoners/'


rito = urllib.request.urlopen(champ_list_url)
response_champs = json.loads(rito.read().decode("utf-8"))
champs = response_champs['data']

rito = urllib.request.urlopen(item_list_url)
response_items = json.loads(rito.read().decode("utf-8"))
items = response_items['data']

rito = urllib.request.urlopen(map_data_url)
response_map = json.loads(rito.read().decode("utf-8"))
maps = response_map['data']

rito = urllib.request.urlopen(summoner_list_url)
response_summoners = json.loads(rito.read().decode("utf-8"))
summoners = response_summoners['data']

### Get champ square (portrait)
for i in champs:
	champ_square = i+'.png' ### Could also be response_champs['data'][i]
	champ_square_url = 'http://ddragon.leagueoflegends.com/cdn/5.10.1/img/champion/%s' % champ_square
	if not os.path.exists(champ_square_path+champ_square):
		urllib.request.urlretrieve(champ_square_url, champ_square_path+champ_square)

### Get skill icons
for i in champs:
	for counter in range(4):
		skill_icon = response_champs['data'][i]['spells'][counter]['image']['full']
		skill_icon_url = 'http://ddragon.leagueoflegends.com/cdn/5.10.1/img/spell/%s' % skill_icon
		if not os.path.exists(skill_path+skill_icon):
			urllib.request.urlretrieve(skill_icon_url, skill_path+skill_icon)

### Get item icons
for i in items:
	item_icon = response_items['data'][i]['image']['full']
	item_icon_url = 'http://ddragon.leagueoflegends.com/cdn/5.10.1/img/item/%s' % item_icon
	if not os.path.exists(item_path+item_icon):
		urllib.request.urlretrieve(item_icon_url, item_path+item_icon)

### Get passive icons
for i in champs:
	passive_icon = response_champs['data'][i]['passive']['image']['full']
	passive_icon_url = 'http://ddragon.leagueoflegends.com/cdn/5.10.1/img/passive/%s' % passive_icon 
	if not os.path.exists(passive_path+passive_icon):
		urllib.request.urlretrieve(passive_icon_url, passive_path+passive_icon)

### Get summoner spell icons
for i in summoners:
	summoner_icon = response_summoners['data'][i]['image']['full']
	summoner_icon_url = 'http://ddragon.leagueoflegends.com/cdn/5.10.1/img/spell/%s' % summoner_icon
	if not os.path.exists(summoner_path+summoner_icon):
		urllib.request.urlretrieve(summoner_icon_url, summoner_path+summoner_icon)

import mysql_loader
