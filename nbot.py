import yaml
import discord
from discord.ext import commands
from discord import Game
import logging
from api_call import iquidusExplorer_bal, iquidusExplorer_diff, iquidusExplorer_nethash, bytes_2_human_readable, coinMapper_bal, coinMapper_diff, coinMapper_nethash, UExplorer_bal, UExplorer_diff, UExplorer_nethash, unknown_coin, MN_ready

logging.basicConfig(level=logging.INFO)

with open('config.yml') as c:
    config = yaml.load(c)



BOT_PREFIX = ("?")

bot = commands.Bot(command_prefix=BOT_PREFIX)

#def is_channel(channel_id):
#	def predicate(ctx):
#		return ctx.message.channel.id == channel_id
#	return commands.check(predicate)
#def listen_channel():
#	if ctx.message.channel != bot.get_channel(config['listen']):
#		await ctx.send("{0.author.mention} hit me up over at {1.mention}".format(ctx, bot.get_channel(config['listen']))) 
#		return(1)
#	else:
#		return(0)

@bot.command(name='coins',
		description="list of coins this bot can help with",
		brief="list of coins this bot can help with")
#@is_channel(464885086559404033)
async def coins(ctx):
	print('channel = ' + str(ctx.message.channel))
	if ctx.message.channel == bot.get_channel(config['listen']):
	#if listen_channel():
		coin_list = []
		for coin in sorted(config['coins']):
			coin_list.append(coin)
		await ctx.send("coins : %s" % coin_list)
	else:
		await ctx.send("{0.author.mention} hit me up over at {1.mention}".format(ctx, bot.get_channel(config['listen']))) 



@bot.command(name='status',
		description="how many coins are ready for the next MasterNode",
		brief="how many coins are ready for the next MasterNode")
async def status(ctx, coin: str):
	if ctx.message.channel == bot.get_channel(config['listen']):
		ucoin = coin.upper()
		if ucoin == 'ALL':
			for c in sorted(config['coins']):
				if config['coins'][c]['explorer'] == 'iquidusExplorer':
					error, balance = iquidusExplorer_bal(config['coins'][c]['site'], config['coins'][c]['wallet'])
				elif config['coins'][c]['explorer'] == 'coinmapper':
					error, balance = coinMapper_bal(c, config['coins'][c]['site'], config['coins'][c]['wallet'])
				else:
					error, balance = UExplorer_bal(config['coins'][c]['site'], config['coins'][c]['wallet'])
	
				if error == 0:
					await ctx.send(c + ' ' + balance + '/' + str(config['coins'][c]['mn_needed']))
			
					if int(balance) >= config['coins'][c]['mn_needed']:
						await ctx.send(MN_ready(ctx, c, config['admin']))
				else:
					await ctx.send('got the following error for ' + c + ': ' + balance)
	
		elif ucoin in config['coins']:
			if config['coins'][ucoin]['explorer'] == 'iquidusExplorer':
				error, balance = iquidusExplorer_bal(config['coins'][ucoin]['site'], config['coins'][ucoin]['wallet'])
			elif config['coins'][ucoin]['explorer'] == 'coinmapper':
				error, balance = coinMapper_bal(ucoin, config['coins'][ucoin]['site'], config['coins'][ucoin]['wallet'])
			else:
				error, balance = UExplorer_bal(config['coins'][ucoin]['site'], config['coins'][ucoin]['wallet'])
		
			if error == 0:
				await ctx.send(ucoin + ' ' + balance + '/' + str(config['coins'][ucoin]['mn_needed']))
				if int(balance) >= config['coins'][ucoin]['mn_needed']:
					await ctx.send(MN_ready(ctx, ucoin, config['admin']))
			else:
				await ctx.send('got the following error for ' + ucoin + ': ' + balance)
		else:	
			await ctx.send(unknown_coin(ctx, coin))
	else:
		await ctx.send("{0.author.mention} hit me up over at {1.mention}".format(ctx, bot.get_channel(config['listen'])))

@bot.command(name='diff',
		aliases=['netdiff', 'difficulty'],
		description="diff for the coin",
		brief="diff for the coin")
async def diff(ctx, *, coin: str):
	if ctx.message.channel == bot.get_channel(config['listen']):
		ucoin = coin.upper()
		if ucoin in config['coins']:
			if config['coins'][ucoin]['explorer'] == 'iquidusExplorer':
				error, diff = iquidusExplorer_diff(config['coins'][ucoin]['site'])
			elif config['coins'][ucoin]['explorer'] == 'coinmapper':
				error, diff = coinMapper_diff(ucoin, config['coins'][ucoin]['site'])
			else:
				error, diff = UExplorer_diff(config['coins'][ucoin]['site'])
			if error == 0:
				await ctx.send(ucoin + ' diff = ' + str(diff))
			else:
				await ctx.send(ucoin + ' error: ' + diff)
		else:
			await ctx.send(unknown_coin(ctx, coin))
	else:
		await ctx.send("{0.author.mention} hit me up over at {1.mention}".format(ctx, bot.get_channel(config['listen'])))

@bot.command(name='nethash',
		aliases=['hash', 'net'],
		description="to show net hash for the coin",
		brief="to show net hash for the coin")
async def nethash(ctx, *, coin: str):
	if ctx.message.channel == bot.get_channel(config['listen']):
		ucoin = coin.upper()
		if ucoin in config['coins']:
			if config['coins'][ucoin]['explorer'] == 'iquidusExplorer':
				error, nethash = iquidusExplorer_nethash(config['coins'][ucoin]['site'])
			elif config['coins'][ucoin]['explorer'] == 'coinmapper':
				error, nethash = coinMapper_nethash(ucoin, config['coins'][ucoin]['site'])
			else:
				error, nethash = UExplorer_nethash(config['coins'][ucoin]['site'])
			if error == 0:
				await ctx.send(ucoin + ' nethash = ' + str(nethash))
			else:
				await ctx.send(ucoin + ' error: ' + nethash)
		else:
			await ctx.send(unknown_coin(ctx, coin))
	else:
		await ctx.send("{0.author.mention} hit me up over at {1.mention}".format(ctx, bot.get_channel(config['listen'])))

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
	if ctx.message.channel == bot.get_channel(config['listen']):
		url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
		async with aiohttp.ClientSession() as session:  # Async HTTP request
			raw_response = await session.get(url)
			response = await raw_response.text()
			response = json.loads(response)
			await ctx.send(" Bitcoin price is: $" + response['bpi']['USD']['rate'])
	else:
		await ctx.send("{0.author.mention} hit me up over at {1.mention}".format(ctx, bot.get_channel(config['listen'])))


async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


bot.loop.create_task(list_servers())
bot.run(config['token'])
