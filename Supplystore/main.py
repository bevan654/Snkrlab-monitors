import requests
import json
import bs4
from bs4 import *
import lxml
import termcolor
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import discord 
from discord.ext import commands
from threading import Thread

class Supplystore_Monitor():
	def __init__(self):
		self.stock = self.LoadJson('stock.json')
		self.proxies = self.loadProxies('proxies.txt')
		self.proxies2 = []
		self.config = self.LoadJson('config.json')
		self.proxyLoop = None

		try:
			self.list_len = len(self.proxies)
		except:
			pass

	def add_product(self,link):
		if 'https' not in link:
			return 'Failed'

		retreive_product = False
		while not retreive_product:
			try:
				response = requests.get(str(link),proxies=self.get_proxy())
				retreive_product = True
			except Exception as e:
				print(e)
				print('[-] Banned')
				continue



		if response.status_code == 200:
			soup = BeautifulSoup(response.content,'lxml')

			title = soup.find('div',attrs={'class':'columns large-4 product-copy'}).find('h3').text
			sku = soup.find('input',attrs={'name':'sku'})['value']

			sizes = soup.find('select',attrs={'id':'Form_Form_Options_Size'}).find_all('option')

			self.stock[str(title)] = {}

			placeholder = {}

			for i in sizes:
				placeholder[str(i['value'])] = i.text

			self.stock[str(title)]['sizes'] = placeholder
			self.stock[str(title)]['link'] = str(link)
			self.stock[str(title)]['image'] = 'http://supplystore.com.au/images/items/'+str(sku)+'/1.jpg' 

			self.SaveJson('stock.json',self.stock)
			return 'Added Product'


		elif response.status_code != 200:
			print('Unknown Error [{}]'.format(response.status_code))
			return 'Unknown Error [{}]'.format(response.status_code)


	def monitor_products(self):
		while True:
			time.sleep(10)
			self.stock = self.LoadJson('stock.json')
			for shoe in self.stock:
				restock = False
				desc = ''
				try:
					t = time.time()
					response = requests.get(str(self.stock[shoe]['link']),proxies=self.get_proxy())
				except Exception as e:
					print(e)
					print('[-] Banned')

				if response.status_code == 200:
					s = time.time()
					total = s-t
					print(total)
					print(str(shoe))

					soup = BeautifulSoup(response.content,'lxml')

					sizes = soup.find('select',attrs={'id':'Form_Form_Options_Size'}).find_all('option')

					for i in sizes:
						if i.text != self.stock[shoe]['sizes'][i['value']]:
							self.stock[shoe]['sizes'][i['value']] = i.text

							restock = True
							button = soup.find('input',attrs={'id':'Form_Form_action_doform'})

							if button == None:
								button_status = 'Disabled'
							else:
								button_status = 'Enabled'

							skus = soup.find('select',attrs={'id':'variantSku'}).find_all('option')

							for k in skus:
								if int(k['available']) <= 0:
										stock_check = '🔴 '
								else:
									stock_check = '🟢 '

								desc = desc + stock_check + '**'+str(k['size']) +'**'+  ' ['+str(k['available'])+']\n'

					if restock:
						self.SaveJson('stock.json',self.stock)
						if self.send_webhook(str(shoe),str(self.stock[shoe]['link']),str(self.stock[shoe]['image']),str(desc),str(button_status),None):
							print('Webhook sent')


					

				elif response.status_code != 200:
					print('[-] Unknown Error [{}]'.format(str(response.status_code)))
					continue
	def get_proxy(self):

		if self.proxies2 == []:
			self.proxyLoop = 'Proxy1'

		elif self.proxies == []:
			self.proxyLoop = 'Proxy2'


		if self.proxyLoop == 'Proxy1':
			proxy = self.proxies[random.randint(0,len(self.proxies)-1)]
			self.proxies.remove(proxy)
			self.proxies2.append(proxy)
		elif self.proxyLoop == 'Proxy2':
			proxy = self.proxies2[random.randint(0,len(self.proxies2)-1)]
			self.proxies2.remove(proxy)
			self.proxies.append(proxy)


		return proxy


	def SaveJson(self,file,data):
		with open(str(file),'w') as e:
			json.dump(data,e,indent=4,sort_keys=True)

	def LoadJson(self,file):
		with open(str(file)) as e:
			try:
				file = json.load(e)
			except:
				file = {}

		return file


	def send_webhook(self,title,link,image,stock_data,button,type):
		webhook = 'https://discord.com/api/webhooks/803451358979686410/E7Er2HZgUXAQ_FeNZ0GYqo3FQKEKoG-Egs6mn4k4kzx5QcboALUXsVeNfrv_s06_C9Np'
		webhook = DiscordWebhook(url=webhook)
		embed = DiscordEmbed(title=str(title), description=None, url=str(link),color=242424)
		embed.set_author(name='https://www.supplystore.com.au/')
		embed.set_thumbnail(url=str(image))
		embed.set_footer(text='Powered by NerdMonitors | By Bevan#7812',icon_url = 'https://images-ext-1.discordapp.net/external/bNNNfSQVbSNx2K4GLbPn-71WgWkzoSpPHJ-M4_6G5tc/https/media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
		embed.set_timestamp()
		add = "```document.getElementById('product-form').submit()```"
		embed.add_embed_field(name='Sizes', value=str(stock_data))
		embed.add_embed_field(name='ATC',value=str(button))
		embed.add_embed_field(name='Scripts',value=str(add),inline=False)
		embed.add_embed_field(name='Links',value='[Login](https://www.supplystore.com.au/shop/login.aspx) | [Cart](https://www.supplystore.com.au/shop/checkout/cart.aspx)\n',inline=False)
		webhook.add_embed(embed)
		response = webhook.execute()
		return True


	def loadProxies(self,file):
		a = []
		with open(str(file)) as e:
			proxies = e.read().splitlines()
			for i in proxies:
				proxy = i.split(':')
				proxy = {
					'http':'http://{}:{}@{}:{}'.format(proxy[2],proxy[3],proxy[0],proxy[1]),
					'https':'https://{}:{}@{}:{}'.format(proxy[2],proxy[3],proxy[0],proxy[1])
				}

				a.append(proxy)

		if a == []:
			return None
		else:
			return a

	def discord(self,token):
		client = commands.Bot(command_prefix = '-nerd supplystore ')
		@client.event
		async def on_ready():
			print('[-] Supplystore Initated - Bot logged in')
		@client.command()
		async def add(message,link):
			t = self.add_product(str(link))
			await message.channel.send(str(t))

		client.run(token)



t = Supplystore_Monitor()
Thread(target=t.monitor_products).start()
t.discord('ODA3MjU0NzU3Njk3NTE5NjE2.YB1UlA.KPZUjtP7fFUHTH_q59zV4QGs-co')
