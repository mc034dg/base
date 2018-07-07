import yaml
import discord
import requests
import requests.exceptions
from discord.ext import commands
from bs4 import BeautifulSoup
import random
import asyncio
import aiohttp
import json
from discord import Game
#from discord.ext.commands import Bot
import logging

logging.basicConfig(level=logging.INFO)

with open('config.yml') as c:
    config = yaml.load(c)


#	'folm': ('https://folm.uexplorer.me/wallets/', 'FZPchqX7pY8AEABrHHuFwTqJHttN3r7YJW', 5000),

BOT_PREFIX = ("?")

bot = commands.Bot(command_prefix=BOT_PREFIX)

def coinMapper_bal(coin, mn_needed, site, wallet):
	try:
		url = site + coin + '/address/' + wallet
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		bal = soup.find_all(class_="col-9 text-truncate p-2")[1]
		b = bal.get_text()
		ba = b.strip('\'')
		return[0, coin + ' ' + ba.split('.')[0] + '/' + mn_needed]
	except requests.exceptions.RequestException as e:
		return[1, coin + ':' + str(e)]

def coinMapper_nethash(coin, site):
	try:
		url = site + coin 
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		h = soup.find_all(class_="card-text text-dark")[0]
		ha = h.get_text()
		has = ha.strip()
		hash = has.strip('\'')
		return[0, coin + ' nethash = ' + hash]
	except requests.exceptions.RequestException as e:
		return[1, coin + ':' + str(e)]

def coinMapper_diff(coin, site):
	try:
		url = site + coin 
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, 'html.parser')
		d = soup.find_all(class_="card-text text-dark")[1]
		di = d.get_text()
		dif = di.strip()
		diff = dif.strip('\'')
		return[0, coin + ' diff = ' + diff]
	except requests.exceptions.RequestException as e:
		return[1, coin + ':' + str(e)]

def iquidusExplorer_bal(coin, mn_needed, site, wallet):
	try:
		url = site + 'ext/getbalance/' + wallet
		response = requests.get(url, timeout=5)
		data = response.json()
		return[0, coin + ' ' + str(int(data)) + '/' + mn_needed]
	except requests.exceptions.RequestException as e:
		return[1, coin + ':' + str(e)]

def iquidusExplorer_diff(coin, site):
	try:
		url = site + 'api/getdifficulty'
		response = requests.get(url, timeout=5)
		data = response.json()
		return[0, coin + ' diff = ' + str('%.3f'%(data))]
	except requests.exceptions.RequestException as e:
		return[1, coin + ' error: ' + str(e)]

def iquidusExplorer_nethash(coin, site):
	try:
		url = site + 'api/getnetworkhashps'
		response = requests.get(url, timeout=5)
		data = response.json()
		hash = bytes_2_human_readable(data)
		return[0, coin + ' net hash = ' + hash]
	except requests.exceptions.RequestException as e:
		return[1, coin + ' error: ' + str(e)]


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

@bot.command(name='coins',
		description="list of coins this bot can help with",
		brief="list of coins this bot can help with")
async def coins(ctx):
		coin_list = []
		for coin in sorted(config['coins']):
			coin_list.append(coin)
		await ctx.send("coins : %s" % coin_list)

@bot.command(name='status',
		description="how many coins are ready for the next MasterNode",
		brief="how many coins are ready for the next MasterNode")
async def status(ctx, coin: str):
		ucoin = coin.upper()
		if ucoin == 'ALL':
			for c in sorted(config['coins']):
				if config['coins'][c]['explorer'] == 'coinmapper':
					error, message = coinMapper_bal(c, str(config['coins'][c]['mn_needed']), config['coins'][c]['site'], config['coins'][c]['wallet'])
				else:
					error, message = iquidusExplorer_bal(c, str(config['coins'][c]['mn_needed']), config['coins'][c]['site'], config['coins'][c]['wallet'])
        	        	
				await ctx.send(message)
	
		elif ucoin in config['coins']:
			if config['coins'][ucoin]['explorer'] == 'coinmapper':
				error, message = coinMapper_bal(ucoin, str(config['coins'][ucoin]['mn_needed']), config['coins'][ucoin]['site'], config['coins'][ucoin]['wallet'])
			else:
				error, message = iquidusExplorer_bal(ucoin, str(config['coins'][ucoin]['mn_needed']), config['coins'][ucoin]['site'], config['coins'][ucoin]['wallet'])
			await ctx.send(message)
		else:	
			await ctx.send('I don\'t know about ' + coin + ' is it a scam?')

@bot.command(name='diff',
		description="diff for the coin",
		brief="diff for the coin")
async def diff(ctx, *, coin: str):
	ucoin = coin.upper()
	if ucoin in config['coins']:
		if config['coins'][ucoin]['explorer'] == 'coinmapper':
			error, message = coinMapper_diff(ucoin, config['coins'][ucoin]['site'])
		else:
			error, message = iquidusExplorer_diff(ucoin, config['coins'][ucoin]['site'])
		await ctx.send(message)
	else:
		await ctx.send('I don\'t know about that coin is it a scam?')

@bot.command(name='nethash',
		description="to show net hash for the coin",
		brief="to show net hash for the coin")
async def nethash(ctx, *, coin: str):
	ucoin = coin.upper()
	if ucoin in config['coins']:
		if config['coins'][ucoin]['explorer'] == 'coinmapper':
			error, message = coinMapper_nethash(ucoin, config['coins'][ucoin]['site'])
		else:
			error, message = iquidusExplorer_nethash(ucoin, config['coins'][ucoin]['site'])
		await ctx.send(message)
	else:
		await ctx.send('I don\'t know about that coin is it a scam?')

#@client.command(name='8ball',
#                description="Answers a yes/no question.",
#                brief="Answers from the beyond.",
#                aliases=['eight_ball', 'eightball', '8-ball'],
#                pass_context=True)
#async def eight_ball(context):
#    possible_responses = [
#        'That is a resounding no',
#        'It is not looking likely',
#        'Too hard to tell',
#        'It is quite possible',
#        'Definitely',
#    ]
#    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)
#

#@client.command()
#async def square(number):
#    squared_value = int(number) * int(number)
#    await client.say(str(number) + " squared is " + str(squared_value))
#

@bot.event
async def on_ready():
#    await client.change_presence(game=Game(name="with the MARTIX"))
    print("Logged in as " + bot.user.name)


@bot.command(name='bitcoin',
		description="report current btc price in USD",
		brief="whats the value today?")
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await ctx.send(" Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


bot.loop.create_task(list_servers())
bot.run(config['token'])
