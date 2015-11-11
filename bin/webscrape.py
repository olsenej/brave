#!/usr/bin/python3
import urllib.request
import urllib.parse
import json
import pprint
import os.path

k = open('apikeyfile', 'r')
apikey = k.read()
k.close()

base_url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2'

ddrag_realm_url = '{0}/realm?api_key={1}'.format(base_url, apikey)
champ_list_url = '{0}/champion?champData=passive,spells&api_key={1}'.format(base_url, apikey)
item_list_url = '{0}/item?itemListData=gold,image,tags&api_key={1}'.format(base_url, apikey)
map_data_url = '{0}/map?api_key={1}'.format(base_url, apikey)
summoner_list_url = '{0}/summoner-spell?spellData=image,modes&api_key={1}'.format(base_url, apikey)
mastery_list_url = '{0}/mastery?masteryListData=image,ranks&api_key={1}'.format(base_url, apikey)

image_base_path = '../images/'
champ_square_path = image_base_path+'portraits/'
skill_path = image_base_path+'skills/'
item_path = image_base_path+'items/'
passive_path = image_base_path+'passives/'
summoner_path = image_base_path+'summoners/'
mastery_path = image_base_path+'masteries/'

rito = urllib.request.urlopen(ddrag_realm_url)
response_ddrag = json.loads(rito.read().decode("utf-8"))
ddrag_version = response_ddrag['dd']
ddrag_cdn = response_ddrag['cdn']

rito = urllib.request.urlopen(champ_list_url)
response_champs = json.loads(rito.read().decode("utf-8"))
champs = response_champs['data']

rito = urllib.request.urlopen(item_list_url)
response_items = json.loads(rito.read().decode("utf-8"))
items = response_items['data']

try:
	rito = urllib.request.urlopen(map_data_url)
	response_map = json.loads(rito.read().decode("utf-8"))
	maps = response_map['data']
	skip_maps=False
except urllib.error.HTTPError:
	skip_maps=True
	pass

rito = urllib.request.urlopen(summoner_list_url)
response_summoners = json.loads(rito.read().decode("utf-8"))
summoners = response_summoners['data']

try: 
	rito = urllib.request.urlopen(mastery_list_url)
	response_masteries = json.loads(rito.read().decode("utf-8"))
	masteries = response_masteries['data']
except urllib.error.URLError as e:
	print(e.reason + " on mastery rerieval")
	masteries = False
	pass

### Get champ square (portrait)
for i in champs:
	champ_square = i+'.png' ### Could also be response_champs['data'][i]
	champ_square_url = '{0}/{1}/img/champion/{2}'.format(ddrag_cdn, ddrag_version, champ_square)
	if not os.path.exists(champ_square_path+champ_square):
		urllib.request.urlretrieve(champ_square_url, champ_square_path+champ_square)

### Get skill icons
for i in champs:
	for counter in range(4):
		skill_icon = response_champs['data'][i]['spells'][counter]['image']['full']
		skill_icon_url = '{0}/{1}/img/spell/{2}'.format(ddrag_cdn, ddrag_version, skill_icon) 
		if not os.path.exists(skill_path+skill_icon):
			urllib.request.urlretrieve(skill_icon_url, skill_path+skill_icon)

### Get item icons
for i in items:
	item_icon = response_items['data'][i]['image']['full']
	item_icon_url = '{0}/{1}/img/item/{2}'.format(ddrag_cdn, ddrag_version, item_icon)
	if not os.path.exists(item_path+item_icon):
		urllib.request.urlretrieve(item_icon_url, item_path+item_icon)

### Get passive icons
for i in champs:
	passive_icon = response_champs['data'][i]['passive']['image']['full']
	passive_icon_url = '{0}/{1}/img/passive/{2}'.format(ddrag_cdn, ddrag_version, passive_icon)
	if not os.path.exists(passive_path+passive_icon):
		urllib.request.urlretrieve(passive_icon_url, passive_path+passive_icon)

### Get summoner spell icons
for i in summoners:
	summoner_icon = response_summoners['data'][i]['image']['full']
	summoner_icon_url = '{0}/{1}/img/spell/{2}'.format(ddrag_cdn, ddrag_version, summoner_icon)
	if not os.path.exists(summoner_path+summoner_icon):
		urllib.request.urlretrieve(summoner_icon_url, summoner_path+summoner_icon)

### Get mastery icons
if masteries != False:
	for i in masteries:
		mastery_icon = response_masteries['data'][i]['image']['full']
		mastery_icon_url = '{0}/{1}/img/mastery/{2}'.format(ddrag_cdn, ddrag_version, mastery_icon)
		if not os.path.exists(mastery_path+mastery_icon):
			urllib.request.urlretrieve(mastery_icon_url, mastery_path+mastery_icon)

import mysql_loader
