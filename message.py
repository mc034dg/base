import yaml
import discord
import asyncio
import aiohttp
import logging
from api_call import iquidusExplorer_bal, iquidusExplorer_diff, iquidusExplorer_nethash, bytes_2_human_readable

logging.basicConfig(level=logging.INFO)

with open('config.yml') as c:
	config = yaml.load(c)

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# create the background task and run it in the background
		self.bg_task = self.loop.create_task(self.my_background_task())

	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')

	async def my_background_task(self):
		await self.wait_until_ready()
		while not self.is_closed():
			for c in sorted(config['coins']):
				print('working on ' + c)
				channel = self.get_channel(config['coins'][c]['discord']) # channel ID goes here
				if config['coins'][c]['explorer'] == 'coinmapper':
					b_error, balance = coinMapper_bal(c, config['coins'][c]['site'], config['coins'][c]['wallet'])
					h_error, hash = coinMapper_nethash(c, config['coins'][c]['site'])
				elif config['coins'][c]['explorer'] == 'UExplorer':
					b_error, balance = UExplorer_bal(config['coins'][c]['site'], config['coins'][c]['wallet'])
					h_error, hash = UExplorer_nethash(config['coins'][c]['site'])
				else:
					b_error, balance = iquidusExplorer_bal(config['coins'][c]['site'], config['coins'][c]['wallet'])
					h_error, hash = iquidusExplorer_nethash(config['coins'][c]['site'])
				if b_error == 0 and h_error == 0 and config['coins'][c]['balance'] != balance and int(balance) >= (config['notify'] * config['coins'][c]['mn_needed']):
					await channel.send('Current Status: ' + balance + ' of ' + str(config['coins'][c]['mn_needed']) + ' coins already deposited for the next masternode with nethash at ' +  hash)
				elif b_error == 1 or h_error == 1:
					print('error getting ' + c + ' stats ' + balance + ' ' + hash)
				elif config['coins'][c]['balance'] == balance:
					print(c + ' balance still ' + balance)
				else:
					print(c + ' ' + balance + ' less then ' + str(config['notify']) + ' percent')
				config['coins'][c]['balance'] = balance
				await asyncio.sleep(60) # task runs every 60 seconds

client = MyClient()
client.run(config['token'])
