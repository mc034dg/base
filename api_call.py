import requests
import requests.exceptions
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json

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