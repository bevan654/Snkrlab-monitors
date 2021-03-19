import requests
import json
import bs4
from bs4 import *
import lxml
import time
from datetime import datetime
import re
from discord_webhook import DiscordWebhook, DiscordEmbed
import discord 
from discord.ext import commands
from threading import Thread
api_au = 'https://www.footlocker.com.au/INTERSHOP/web/WFS/FootlockerAustraliaPacific-Footlocker_AU-Site/en_AU/-/AUD/ViewProduct-ProductVariationSelect'

def oFile(file):
	with open(str(file)) as e:
		try:
			data = json.load(e)
		except:
			data = {}

	return data

def sFile(file,data):
	with open(str(file),'w') as e:
		json.dump(data,e,indent=4,sort_keys =True)



def getSku(link):
    sku = re.sub(r'^.*?v=', '', link)

    return sku

def getTitle(link,sku):
    title = re.sub(r'^.*?/p/', '', link)
    title = title.replace('?v='+str(sku),'')
    title = title.replace('-',' ')
    title = title.title()

    return title

def times():
	now = datetime.now()

	current_time = now.strftime("%H:%M:%S")
	times = '['+str(current_time)+'] '

	return times



headersAU = {
    'authority': 'www.footlocker.com.au',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.footlocker.com.au/en/p/jordan-1-low-infants-shoes-99138?v=246160206004',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'UqZBpD3n3iPIDwJU=v1K0g7Ja+jiad; sid=397ui0SLqilauBtQ4I3kEVEnzwXEuXeSExg3N2kLQHCYqKsVuxWnYiv0; pgid-FootlockerAustraliaPacific-Footlocker_AU-Site=B_paGUcRpNFSRpsI7bemz3z80000HYfXbtru; fl-test-cookie-exist=Exist; fl-notice-cookie=true; country_notify=true; SecureSessionID-PZ2sFf0LwroAAAFbH08RqohB=001c5e675d7252fa976a8bf9efaf0989e1fcedac87adb90aeedae2e8f01e3f60; _ga=GA1.3.1380935725.1608204118; _gid=GA1.3.2063502715.1608204118; _hjTLDTest=1; _hjid=c2ed994e-308c-4354-90fc-4d52eafd83cc; _hjFirstSeen=1; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=0; _crbx=2ca916d7-2395-477d-93ba-1517c44229d6; cc-duSsFf0LxxQAAAFb7FERqohB=gC2sFf0cQiUAAAF2dRL_UXB4; datadome=Dnoz1RJ8TrlMNAa_MmqT-jLJxcM81Oce2IJPrq.sT~tyNesZCmvC14Jof5-zGxP~VM_ahhL3Pee.Mpo.10tSumkeW-e6x5OF~OJ9UkPrEB; OptanonConsent=isIABGlobal=false&datestamp=Thu+Dec+17+2020+22%3A42%3A18+GMT%2B1100+(Australian+Eastern+Daylight+Time)&version=6.6.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A0%2C0_285219%3A1%2C0_285221%3A0%2C0_285220%3A0%2C0_285222%3A0&AwaitingReconsent=false; stc117615=tsa:0:20201217121219|env:1%7C20210117112158%7C20201217121219%7C7%7C1071146:20211217114219|uid:1608204118484.1550945309.748313.117615.416939161.3:20211217114219|srchist:1071146%3A1%3A20210117112158:20211217114219'
}

stock = oFile('stock.json')
config = oFile('config.json')


def send_noti(restock_type,title,sku,data,link):

	webhook = ['https://discord.com/api/webhooks/807781523775946782/YFHrLlhq8MjlpwZPSHt0SPvlHU0yWtIJJAi2xlmdGBmacqwuwKKPLG0tfP1WLwggTQBG','https://discord.com/api/webhooks/807781106815336458/bzVCm-6f1hnK8zKRmrjEWZIj2zF84plRSpF3CdLluD_zjvm8-EFyCniNon4qhKe_UuM5']

	if restock_type == 'restock':
		webhook = DiscordWebhook(url=webhook)
		embed = DiscordEmbed(title=str(title), description=None, color=25500,url=str(link),username='Footlocker AU | By NerdMonitors')

		embed.set_author(name='https://www.footlocker.com.au/')
		embed.set_thumbnail(url='https://images.footlocker.com/is/image/FLEU/'+str(sku)+'_01?wid=763&hei=538&fmt=png-alpha')
		embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
		embed.set_timestamp()
		embed.add_embed_field(name='TYPE',value='RESTOCK',inline=True)
		embed.add_embed_field(name='SKU', value=str(sku),inline=True)
		embed.add_embed_field(name='SIZES', value=str(data),inline=False)
		embed.add_embed_field(name='LINKS',value='[Cart](https://www.footlocker.com.au/en/cart)',inline=False)
		webhook.add_embed(embed)
		response = webhook.execute()
	if restock_type == 'stock_load':
		webhook = DiscordWebhook(url=webhook)
		embed = DiscordEmbed(title=str(title),description=None,color=25500,url=str(link))
		embed.set_author(name='https://www.footlocker.com.au/')
		embed.set_thumbnail(url='https://images.footlocker.com/is/image/FLEU/'+str(sku)+'_01?wid=763&hei=538&fmt=png-alpha')
		embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
		embed.set_timestamp()
		embed.add_embed_field(name='TYPE',value='PRODUCT LOAD',inline=True)
		embed.add_embed_field(name='SKU',value=str(sku),inline=True)
		embed.add_embed_field(name='SIZES',value=str(data),inline=False)
		embed.add_embed_field(name='LINKS',value='[Cart](https://www.footlocker.com.au/en/cart)',inline=False)
		webhook.add_embed(embed)
		response = webhook.execute()

	if restock_type == 'nostock_load':
		webhook = DiscordWebhook(url=webhook)
		embed = DiscordEmbed(title=str(title),description=None,color=25500,url=str(link))
		embed.set_author(name='https://www.footlocker.com.au/')
		embed.set_thumbnail(url='https://images.footlocker.com/is/image/FLEU/'+str(sku)+'_01?wid=763&hei=538&fmt=png-alpha')
		embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
		embed.set_timestamp()
		embed.add_embed_field(name='TYPE',value='PRODUCT LOAD',inline=True)
		embed.add_embed_field(name='SKU',value=str(sku),inline=True)
		embed.add_embed_field(name='SIZES',value=str('Loaded out of stock'),inline=False)
		embed.add_embed_field(name='LINKS',value='[Cart](https://www.footlocker.com.au/en/cart)',inline=False)
		webhook.add_embed(embed)
		response = webhook.execute()

def addProduct(link):
	if 'https' not in str(link):
		return False

	else:
		sold_out = False
		sku = getSku(link)
		title = getTitle(link,sku)

		params = {
			'BaseSKU':str(sku),
			'InventoryServerity':'ProductDetail'
		}

		stock[str(title)] = {}
		stock[str(title)]['link'] = str(link)
		stock[str(title)]['sku'] = str(sku)
		response = requests.get(str(api_au),headers=headersAU,params=params)
		if response.status_code == 410:
			print('Product Page Pulled')
			return False

		elif response.status_code == 503:
			print(times()+'Footlocker Queue Live [Cannot add product]')
			return False
		elif response.status_code != 200:
			print(times()+'Failed connecting to footlocker')

			return False

		elif response.status_code == 200:
			print('[ + ] Adding Product')

			try:
				word_a = "data-product-variation-info-json="
				word_b = r"}}'"

				json_data_start = response.text.index(word_a)
				json_data_end = response.text.index(word_b)
			except:
				try:
					result = re.search('Foot Locker - Sold Out!', response.text)
					v = result.group(0)
					print("All sizes sold out!")

					sold_out = True
				except:
					print(times()+'Error Fetching Product Data....')

			if not sold_out:
				try:
					data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
					data = data.replace("&quot;", "\"")
					data = json.loads(data)
				except:
					print(times()+'Failed to add product')
					return False

				add = {}

				for key in data.keys():
					print(str(data[key]['sizeValue']) + ': ' + str(data[key]['inventoryLevel']))
					add[str(data[key]['sizeValue'])] = str(data[key]['inventoryLevel'])

			stock[str(title)]['sizes'] = add
			sFile('stock.json',stock)
			return True





def checker(delay):
	while True:
		embed = None
		stock = oFile('stock.json')
		if stock == {}:
			print(times()+'No products to monitor')
		else:
			for shoe in stock:
				sold_out = False
				params = {
					'BaseSKU':str(stock[shoe]['sku']),
					'InventoryServerity':'ProductDetail'
				}
				try:
					response = requests.get(str(api_au),headers=headersAU,params=params)
				except:
					print(times()+'Network Error')
					pass
				if response.status_code == 410:
					print('Product Page Pulled')
					pass
				elif response.status_code == 503:
					print(times()+'Footlocker Queue Live [Monitor Disabled][5 Minutes]')
					time.sleep(300)
					pass
				elif response.status_code != 200:
					print(times()+'Failed connecting to footlocker')

					pass

				elif response.status_code == 200:
					print('[ + ]'+times()+'Fetching Product Stock')
					try:
						word_a = "data-product-variation-info-json="
						word_b = r"}}'"

						json_data_start = response.text.index(word_a)
						json_data_end = response.text.index(word_b)
					except:
						try:
							result = re.search('Foot Locker - Sold Out!', response.text)
							v = result.group(0)
							print("All sizes sold out!")

							sold_out = True
						except:
							print(times()+'Error Fetching Product Data.... [No JSON]')
							sold_out = True
							pass

					if not sold_out:
						data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
						data = data.replace("&quot;", "\"")
						data = json.loads(data)

						desc = ''
						for key in data.keys():
							
							if stock[shoe]['sizes'][str(data[key]['sizeValue'])] != data[key]['inventoryLevel']:
								embed = False

								if 'RED' in data[key]['inventoryLevel']:

									stock[shoe]['sizes'][str(data[key]['sizeValue'])] = data[key]['inventoryLevel']

									sFile('stock.json',stock)

								elif 'YELLOW' or 'GREEN' in data[key]['inventoryLevel']:
									print(times()+'Restock')
									stock[shoe]['sizes'][str(data[key]['sizeValue'])] = data[key]['inventoryLevel']

									if 'YELLOW' in data[key]['inventoryLevel']:
										desc = desc + '🟡US'+str(data[key]['sizeValue']) + '\n'
									elif 'GREEN' in data[key]['inventoryLevel']:
										desc = desc + '🟢US'+str(data[key]['sizeValue']) + '\n'
									embed = True

									sFile('stock.json',stock)
						
								
								else:
									pass
						if embed:
							send_noti('restock',str(shoe),str(stock[shoe]['sku']),desc,str(stock[shoe]['link']))

								

		time.sleep(int(delay))


def fetchStock(sku):
	sold_out = False
	params = {
		'BaseSKU':str(sku),
		'InventoryServerity':'ProductDetail'
	}

	response = requests.get(str(api_au),headers=headersAU,params=params)
	if response.status_code == 503:
		print(times()+'Footlocker Queue Live [Monitor Disabled][5 Minute][New Products]')
		return False
	elif response.status_code == 500:
		print(times()+'Internal Server Error [New Products]')
		return False
	elif response.status_code == 403:
		print(times()+'IP Blocked')
		return False
	elif response.status_code != 200:
		print(times()+'Failed connecting to footlocker [New Products]')
		return False
	elif response.status_code == 200:
		print(times()+'Fetching stock')
		try:
			word_a = "data-product-variation-info-json="
			word_b = r"}}'"

			json_data_start = response.text.index(word_a)
			json_data_end = response.text.index(word_b)
		except:
			try:
				result = re.search('Foot Locker - Sold Out!', response.text)
				v = result.group(0)
				print("All sizes sold out!")

				sold_out = True
			except:
				return False
				print(times()+'Error Fetching Product Data....')

		if not sold_out:
			data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
			data = data.replace("&quot;", "\"")
			data = json.loads(data)

			k = {}
			for key in data.keys():
				k[str(data[key]['sizeValue'])] = data[key]['inventoryLevel']

			return k, True
				


def new(delay):
	while True:
		config = oFile('config.json')
		keywords = config['keywords']
		new = oFile('new.json')
		for key in keywords:
			params = {
				'q':str(key)
			}
			try:
				response = requests.get('https://www.footlocker.com.au/en/search',params=params,headers=headersAU)
			except:

				print(times()+'Network Error')
				pass
			if response.status_code == 503:
				print(times()+'Footlocker Queue Live [Monitor Disabled][5 Minute][New Products]')
				time.sleep(300)
				pass
			elif response.status_code == 500:
				print(times()+'Internal Server Error [New Products]')
				pass
			elif response.status_code == 403:
				print(times()+'IP Blocked')
				time.sleep(150)
				pass
			elif response.status_code != 200:
				print(times()+'Failed connecting to footlocker [New Products]')
				time.sleep(150)
				pass
			elif response.status_code == 200:
				print(times()+'Looking for new listings')

				try:
					soup = BeautifulSoup(response.content,'lxml')
				except Exception as e:
					print(e)
					print(times()+'Failed to parse content [New Products]')
					pass

				l = soup.find_all('a')
				for links in l:
					try:
						link = links['href']
					except:
						pass

					if '?v=' in link:
						if 'shoe' in str(link):
							sku = getSku(link)
							title = getTitle(link,sku)
							if str(title) not in new:
								
								new[str(title)] = str(link)
								sFile('new.json',new)

								print(times()+'New product - Checking Stock')
								stock,success = fetchStock(str(sku))
								available_stock = False
								desc = ''

								if success:
									for key,value in stock.items():
										if 'GREEN' in str(value):
											desc = desc +':green_circle:US'+str(key) + '\n'
											available_stock = True
										if 'YELLOW' in str(value):
											desc = desc + ':yellow_circle:US'+str(key)+'\n'
											available_stock = True

								if available_stock:
									send_noti('stock_load',str(title),str(sku),str(desc),str(link))
								else:
									send_noti('nostock_load',str(title),str(sku),None,str(link))
											
											




		time.sleep(int(delay))


							

def bot(token):
	client = commands.Bot(command_prefix='-nerd ')
	@client.event
	async def on_ready():
		print('Logged in')
	@client.command()
	async def products(message):
		stock = oFile('stock.json')

		desc = ''
		for i in stock:
			desc = desc + '['+str(i)+']' +'('+str(stock[i]['link'])+')'+ ' [' + str(stock[i]['sku']) + ']' + '\n'
		
		embed = discord.Embed(title='Product List', description=None, color=0xe91e63,timestamp=datetime.now())
		embed.add_field(name='Products',value=str(desc))
		embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')

		await message.channel.send(embed=embed)

	@client.command()
	async def add(message,link):
		role = discord.utils.get(message.guild.roles, name='Staff')
		if role in message.author.roles:
			embed = discord.Embed(title='Add Product', description=None, color=0xe91e63)
			
			if addProduct(str(link)):
				embed = discord.Embed(title='Add Product', description='Successfully added product', color=0xe91e63)
			else:
				embed = discord.Embed(title='Add Product', description='Failed to add product', color=0xe91e63)
			embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
			await message.channel.send(embed=embed)
		else:
			embed = discord.Embed(title='Invalid Permission', description='Invalid permission to add products, ask a staff member', color=0xe91e63)
			embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
			await message.channel.send(embed=embed)

	@client.command()
	async def delsku(message,sku):
		role = discord.utils.get(message.guild.roles, name='Staff')
		if role in message.author.roles:
			embed = discord.Embed(title='Add Product', description=None, color=0xe91e63)
			found = None
			
			for i in list(stock):
				if str(stock[i]['sku']) == str(sku):
					try:
						stock.pop(i)
						embed = discord.Embed(title='Delete Product', description='Successfully deleted product', color=0xe91e63)
						found = True
						sFile('stock.json',stock)
					except:
						embed = discord.Embed(title='Delete Product', description='Failed to add product', color=0xe91e63)
					embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
					await message.channel.send(embed=embed)

			if not found:
				embed = discord.Embed(title='Delete Product', description='No products found', color=0xe91e63)
				embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
				await message.channel.send(embed=embed)					


						
		else:
			embed = discord.Embed(title='Invalid Permission', description='Invalid permission to add products, ask a staff member', color=0xe91e63)
			embed.set_footer(text='Powered By NerdMonitors | By Bevan#7812',icon_url='https://media.discordapp.net/attachments/806098627406594109/807262072962023434/favpng_nerd-geek-cartoon.png')
			await message.channel.send(embed=embed)

	client.run(token)



		
Thread(target=checker,args={'10'}).start()
Thread(target=new,args={'200'}).start()
bot('ODA3MjU0NzU3Njk3NTE5NjE2.YB1UlA.KPZUjtP7fFUHTH_q59zV4QGs-co')


