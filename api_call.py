import requests
import requests.exceptions
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import random

def MN_ready(context, coin, admin):
	possible_responses = [
		admin + ' ' + coin + ' is ready take us to the moon',
		'chop chop - ' + admin + ' ' + coin,
		'Time to make the MN - ' + admin + ' ' + coin,
		admin + ' we are missing out on rewards for ' + coin,
	]
	return(random.choice(possible_responses))

def unknown_coin(context, coin):
	possible_responses = [
		'I don\'t know about ' + coin + ' is it a scam?',
		context.message.author.mention + ' is there an explorer for ' + coin + '?',
		context.message.author.mention + ' send me 42.35 nlab\'s and the link to the explorer for ' + coin + ' and I will think about adding it',
		context.message.author.mention + ' is it really worth adding ' + coin + ' or will it be dead in a week or two!',
		context.message.author.mention + ' hold my beer and I will add that one',
	]
	return(random.choice(possible_responses))

def UExplorer_nethash(site):
	try:
		url = site + '/api/chart/stat'
		h = requests.get(url, timeout=5)
		ha = h.text
		has = json.loads(ha)
		hash = str(round(has[0]['Network'] / 1000, 2)) 
		return[0, hash + ' Gh/s']
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def UExplorer_diff(site):
	try:
		url = site + '/api/chart/stat'
		d = requests.get(url, timeout=5)
		di = d.text
		dif = json.loads(di)
		return[0, str('%.3f'%(dif[0]['Difficulty']))]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def UExplorer_bal(site, wallet):
	try:
		url = site + '/wallets/' + wallet
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		b = soup.find_all(class_="table table-bordered")[0]
		ba = b.find_all("td")[1]
		bal = ba.get_text()
		bala = bal.strip('\'')
		return[0, bala.split('.')[0]]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def coinMapper_bal(coin, site, wallet):
	try:
		url = site + coin + '/address/' + wallet
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		bal = soup.find_all(class_="col-9 text-truncate p-2")[1]
		b = bal.get_text()
		ba = b.strip('\'')
		return[0, ba.split('.')[0]]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def coinMapper_nethash(coin, site):
	try:
		url = site + coin 
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		h = soup.find_all(class_="card-text text-dark")[0]
		ha = h.get_text()
		has = ha.strip()
		hash = has.strip('\'')
		return[0, hash]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def coinMapper_diff(coin, site):
	try:
		url = site + coin 
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		d = soup.find_all(class_="card-text text-dark")[1]
		di = d.get_text()
		dif = di.strip()
		diff = dif.strip('\'')
		return[0, diff]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def iquidusExplorer_bal(site, wallet):
	try:
		url = site + 'ext/getbalance/' + wallet
		response = requests.get(url, timeout=5)
		data = response.json()
		return[0, str(int(data))]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def iquidusExplorer_diff(site):
	try:
		url = site + 'api/getdifficulty'
		response = requests.get(url, timeout=5)
		data = response.json()
		return[0, str('%.3f'%(data))]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]

def iquidusExplorer_nethash(site):
	try:
		url = site + 'api/getnetworkhashps'
		response = requests.get(url, timeout=5)
		data = response.json()
		hash = bytes_2_human_readable(data)
		return[0, hash]
	except requests.exceptions.RequestException as e:
		return[1, str(e)]


def bytes_2_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'H/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'Kh/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'Mh/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'Gh/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'Th/s'

    precision = 3
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit
