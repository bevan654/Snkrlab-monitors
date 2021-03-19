import requests
import bs4
from bs4 import *
import lxml
import json
import asyncio
import termcolor
from termcolor import *
import colorama
from datetime import datetime
import re
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import Thread
class Main:

    @classmethod
    def fprint(self,text,color):
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        current_time = '[{}] '.format(str(current_time))

        print(colored('{}'.format(current_time)+str(text),'{}'.format(str(color))))

    @classmethod
    def openJson(self,folder,file):
        try:

            with open('{}/{}'.format(str(folder),str(file)),'r') as e:
                try:
                    json_file = json.load(e)
                except Exception as e:
                    json_file = {}
                    pass

            return json_file

        except Exception as e:
            print(e)
            return

    @classmethod
    def saveJson(self,folder,file,data):
        result = None
        try:
            with open('{}/{}'.format(str(folder),str(file)),'w') as e:
                try:
                    json.dump(data,e,indent=4,sort_keys=True)
                    result = True
                except Exception as e:
                    print(e)
                    result = False

        except Exception as e:
           print(e)

        finally:
            return result

    @classmethod
    def startDiscord(self,token):
        Main.fprint('Starting Discord Bot')
        client = commands.Bot(command_prefix='-')
        @client.event
        async def on_ready():
            print('Logged in')
        @client.command()
        async def footlocker(message,link):
            await message.channel.send(Footlocker.add_product(str(link)))

        client.run(token)


class Footlocker:
    def __init__(self):
        self.headers = {
            'authority': 'www.footlocker.com.au',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'Cache-Control':'max-age=0',
            'referer': 'https://www.footlocker.com.au/en/p/jordan-1-low-infants-shoes-99138?v=246160206004',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'UqZBpD3n3iPIDwJU=v1K0g7Ja+jiad; sid=397ui0SLqilauBtQ4I3kEVEnzwXEuXeSExg3N2kLQHCYqKsVuxWnYiv0; pgid-FootlockerAustraliaPacific-Footlocker_AU-Site=B_paGUcRpNFSRpsI7bemz3z80000HYfXbtru; fl-test-cookie-exist=Exist; fl-notice-cookie=true; country_notify=true; SecureSessionID-PZ2sFf0LwroAAAFbH08RqohB=001c5e675d7252fa976a8bf9efaf0989e1fcedac87adb90aeedae2e8f01e3f60; _ga=GA1.3.1380935725.1608204118; _gid=GA1.3.2063502715.1608204118; _hjTLDTest=1; _hjid=c2ed994e-308c-4354-90fc-4d52eafd83cc; _hjFirstSeen=1; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=0; _crbx=2ca916d7-2395-477d-93ba-1517c44229d6; cc-duSsFf0LxxQAAAFb7FERqohB=gC2sFf0cQiUAAAF2dRL_UXB4; datadome=Dnoz1RJ8TrlMNAa_MmqT-jLJxcM81Oce2IJPrq.sT~tyNesZCmvC14Jof5-zGxP~VM_ahhL3Pee.Mpo.10tSumkeW-e6x5OF~OJ9UkPrEB; OptanonConsent=isIABGlobal=false&datestamp=Thu+Dec+17+2020+22%3A42%3A18+GMT%2B1100+(Australian+Eastern+Daylight+Time)&version=6.6.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A0%2C0_285219%3A1%2C0_285221%3A0%2C0_285220%3A0%2C0_285222%3A0&AwaitingReconsent=false; stc117615=tsa:0:20201217121219|env:1%7C20210117112158%7C20201217121219%7C7%7C1071146:20211217114219|uid:1608204118484.1550945309.748313.117615.416939161.3:20211217114219|srchist:1071146%3A1%3A20210117112158:20211217114219'
        }

        self.api_link = 'https://www.footlocker.com.au/INTERSHOP/web/WFS/FootlockerAustraliaPacific-Footlocker_AU-Site/en_AU/-/AUD/ViewProduct-ProductVariationSelect'
        self.products = Main.openJson('Footlocker_AU','stock.json')
        self.new_listing = Main.openJson('Footlocker_AU','new_listing.json')
        self.sitemap = Main.openJson('Footlocker_AU','sitemap.json')
        self.config = Main.openJson('Footlocker_AU','config.json')

        Thread(target=self.monitor).start()
        self.listings()

        Main.fprint('Footlocker Monitor Initated - Loading Discord Bot','yellow')
    def error(self,err):
        self.errorhook = 'https://discord.com/api/webhooks/820257030689390632/uBMgVkpvoTdmqLmTreB2Dc3Uxh8bhYKy_gNtZ3egwxE3UkYC6LnOhATQUETdPfvxf8r9'

        webhook = DiscordWebhook(url=self.errorhook)
        embed = DiscordEmbed(title='Footlocker AU',description=str(err))
        embed.set_author(name='https://www.footlocker.com.au/')
        embed.set_timestamp()
        embed.set_footer(text='SNKRLab Technologies')
        webhook.add_embed(embed)
        try:
            response = webhook.execute()
        except Exception as e:
            Main.fprint('{} - Most Likely Network Error'.format(str(e)),'red')
    def send_webhook(self,channel,sku,title,url,notification_type,data):
        
        webhooks = self.config['webhooks']
        if channel == 'footlocker-au':
            webhook = DiscordWebhook(url=webhooks['footlocker-au'])
        elif channel == 'footlocker-queue':
            webhook = DiscordWebhook(url=webhooks['footlocker-queue'])

        if notification_type == 'restock':
            embed = DiscordEmbed(title=str(title),description=None,url=str(url))
            embed.set_author(name='https://www.footlocker.com.au/')
            embed.set_thumbnail(url='https://images.footlocker.com/is/image/FLEU/{}_01?wid=763&hei=538&fmt=png-alpha'.format(str(sku)))
            embed.set_footer(text='SNKRLab Monitors',icon_url='https://media.discordapp.net/attachments/815187995271102465/818751424401899561/unknown.png?width=699&height=364')
            embed.set_timestamp()
            embed.add_embed_field(name='TYPE',value='RESTOCK',inline=True)
            embed.add_embed_field(name='SKU',value=str(sku),inline=True)
            embed.add_embed_field(name='SIZES',value=str(data),inline=False)
            embed.add_embed_field(name='LINKS',value='[Cart]({})'.format('https://footlocker.com.au/cart'))    
            webhook.add_embed(embed)
            response = webhook.execute()    
        if notification_type == 'queue':
            embed = DiscordEmbed(title='Footlocker AU',description='Queue Live')
            embed.set_author(name='https://www.footlocker.com.au/')
            embed.set_footer(text='SNKRLab Monitors',icon_url='https://media.discordapp.net/attachments/815187995271102465/818751424401899561/unknown.png?width=699&height=364')
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()

        if notification_type == 'load':
            embed = DiscordEmbed(title=str(title),description=None,url=str(url))
            embed.set_author(name='https://www.footlocker.com.au/')
            embed.set_thumbnail(url='https://images.footlocker.com/is/image/FLEU/{}_01?wid=763&hei=538&fmt=png-alpha'.format(str(sku)))
            embed.set_footer(text='SNKRLab Monitors',icon_url='https://media.discordapp.net/attachments/815187995271102465/818751424401899561/unknown.png?width=699&height=364')
            embed.set_timestamp()
            embed.add_embed_field(name='TYPE',value='LOAD',inline=True)
            embed.add_embed_field(name='SKU',value=str(sku),inline=True)
            embed.add_embed_field(name='SIZES',value=str(data),inline=False)
            embed.add_embed_field(name='LINKS',value='[Cart]({})'.format('https://footlocker.com.au/cart'))    
            webhook.add_embed(embed)
            response = webhook.execute()    
    def fetchStock(self,sku):
        sold_out = False
        params = {
            'BaseSKU':str(sku),
            'InventoryServerity':'ProductDetail'
        }

        response = requests.get(str(self.api_link),headers=self.headers,params=params)
        if response.status_code == 503:
            print('Footlocker Queue Live [Monitor Disabled][5 Minute][New Products]')
            return False
        elif response.status_code == 500:
            print('Internal Server Error [New Products]')
            return False
        elif response.status_code == 403:
            print('IP Blocked')
            return False
        elif response.status_code != 200:
            print('Failed connecting to footlocker [New Products]')
            return False
        elif response.status_code == 200:
            print('Fetching stock')
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
                    return 'sold_out'
                except:
                    return False
                    print('Error Fetching Product Data....')

            if not sold_out:
                data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
                data = data.replace("&quot;", "\"")
                data = json.loads(data)

                k = {}
                for key in data.keys():
                    k[str(data[key]['sizeValue'])] = data[key]['inventoryLevel']

                return k
    def add_product(self,link):
        sold_out = None
        if 'https' not in str(link):
            if len(str(link)) == 12:
                sku_input = True
            else:
                return 'Invalid Link/SKU'
        else:
            sku_input = False

        if sku_input:
            sku = link
            title = link
            link = 'https://footlocker.com.au/?q={}'.format(str(sku))
        else:
            sku = self.getSku(link)
            title = self.getTitle(link,sku)
            link = link

        print(sku_input)
        #print(insert_link)
    

        params = {
			'BaseSKU':str(sku),
			'InventoryServerity':'ProductDetail'
		}

        try:
            response = requests.get(str(self.api_link),headers=self.headers,params=params)
            #print(response.content)
        except Exception as e:
            Main.fprint(str(e) + '[Line 114] - Most Likely a network error','red')
            return 'Could not add product'

        if response.status_code == 200:
            Main.fprint('Adding Product','yellow')

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

                    if sold_out:
                        self.products[str(title)] = {'sku':str(sku),'sizes':{},'page_status':'sold_out','link':str(link)}
                        Main.saveJson('Footlocker_AU','stock.json',self.products)
                except Exception as e:
                    print(e)
                    return 'Error retrieving product json'

            if not sold_out:
                try:
                    data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
                    data = data.replace("&quot;", "\"")
                    data = json.loads(data)
                except:
                    Main.fprint('Failed to add product','red')
                    return False

                add = {}

                for key in data.keys():
                    print(str(data[key]['sizeValue']) + ': ' + str(data[key]['inventoryLevel']))
                    add[str(data[key]['sizeValue'])] = str(data[key]['inventoryLevel'])

                self.products[str(title)] = {'sku':str(sku),'sizes':add,'page_status':'live','link':str(link)}
                
                Main.saveJson('Footlocker_AU','stock.json',self.products)
                Main.fprint('Successfully added product','green')
                return 'Successfully added product'

            

        elif response.status_code == 503:
            return 'Footlocker Queue Live'
        elif response.status_code == 429:
            return 'Rate Limit'
        elif response.status_code != 200:
            return 'Unkown Status Code {}'.format(str(response.status_code))
    def monitor(self):
        Main.fprint('Monitor Initiated','yellow')
        t = True
        while t:
            self.delay = self.config['delay']
            time.sleep(self.delay)
            self.products = Main.openJson('Footlocker_AU','stock.json')
            if self.products == {}:
                Main.fprint('No Products Found to montior','yellow')
                time.sleep(self.delay)
                continue
            else:
                for product in self.products:
                    sold_out = None

                    sku = self.products[product]['sku']
                    
                    params = {
                        'BaseSKU':str(sku),
                        'InventoryServerity':'ProductDetail'
                    }

                    try:
                        response = requests.get(str(self.api_link),headers=self.headers,params=params)
                    except Exception as e:
                        self.error(str(e))

                    if response.status_code == 200:
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
                                self.products[product]['page_status'] = 'sold_out'
                            except Exception as e:
                                print(e)
                                Main.fprint('Could not find json','red')

                        if not sold_out and self.products[product]['page_status'] == 'sold_out':
                            self.products[product]['page_status'] = 'live'
                            try:
                                data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
                                data = data.replace("&quot;", "\"")
                                data = json.loads(data)
                            except Exception as e:
                                Main.fprint('{} - Line 250'.format(e),'red')

                            product_data = ''
                            add = {}
                            for key in data.keys():
                                add[str(data[key]['sizeValue'])] = str(data[key]['inventoryLevel'])

                                
                                if 'GREEN' in data[key]['inventoryLevel']:
                                    product_data = product_data + ':green_circle:{}'.format(str(data[key]['sizeValue'])) + '\n'
                                elif 'YELLOW' in data[key]['inventoryLevel']:
                                    product_data = product_data + ':yellow_circle:{}'.format(str(data[key]['sizeValue'])) + '\n'
                                else:
                                    data = data


                            self.products[str(product)]['sizes'] = add
                            KMain.fprint('Restock Detected - 272')
                        elif not sold_out and self.products[product]['page_status'] == 'live':
                            try:
                                data = "{" + response.text[(json_data_start + len(word_a) + 2) : json_data_end] + "}}"
                                data = data.replace("&quot;", "\"")
                                data = json.loads(data)
                            except Exception as e:
                                Main.fprint('{} - Line 250'.format(e),'red')

                            product_data = ''
                            embed = None
                            for key in data.keys():
                                if data[key]['inventoryLevel'] != self.products[product]['sizes'][str(data[key]['sizeValue'])]:
                                    self.products[product]['sizes'][str(data[key]['sizeValue'])] = str(data[key]['inventoryLevel'])
                                    Main.saveJson('Footlocker_AU','stock.json',self.products)


                                    if 'GREEN' or 'YELLOW' in data[key]['inventoryLevel']:
                                        product_data = product_data + ':green_circle::yellow_circle:{}'.format(str(data[key]['sizeValue'])) + '\n'
                                        embed = True
                                    else:
                                        pass

                            if embed:
                                Main.fprint('restock detected - 295','green')
                                self.send_webhook('footlocker-au',str(sku),str(product),str(self.products[product]['link']),'restock',product_data)




                            
                    elif response.status_code == 503:
                        self.error('Queue Live')
                        self.send_webhook('footlocker-queue',True,True,True,'queue',None)
                        time.sleep(300)
                        continue

                    elif response.status_code == 410:
                        Main.fprint('Product Page Pulled [{}]'.fomrat(product),'red')
                        continue
                    elif response.status_code != 200:
                        self.error('Bad response status [{}]'.format(str(response.status_code)))

                    '''
                    sku_input = None
                    link = self.products[product]['link']
                    if 'https' not in link:
                        if len(str(link)) == 12:
                            sku_input = True
                            sku = str(link)
                        else:
                            Main.fprint('Bad link','red')
                            continue
                    else:
                        pass

                    if not sku_input:
                        sku = self.products[product]['sku']
                    '''
    def listings(self):
        while True:
        
            keywords = self.config['keywords']
            for key in keywords:
                time.sleep(3)
                params = {
                    'q':str(key)
                }

                try:
                    response = requests.get('https://www.footlocker.com.au/en/search',params=params,headers=self.headers)
                except Exception as e:
                    Main.fprint('{} - Most Likely A network Error [364]'.format(str(e)),'red')
                    self.error(str(e))
                    continue

                if response.status_code == 200:
                    Main.fprint('Looking for new listings','yellow')

                    soup = BeautifulSoup(response.content,'lxml')
                    l = soup.find_all('a')
                    for links in l:
                        try:
                            link = links['href']
                        except:
                            pass

                        if '?v=' in link:
                            if 'shoe' in str(link):
                                sku = self.getSku(link)
                                title = self.getTitle(link,sku)
                                if str(title) not in self.new_listing:
                                    
                                    self.new_listing[str(title)] = str(link)
                                    Main.saveJson('Footlocker_AU','new_listing.json',self.new_listing)

                                    print('New product - Checking Stock')
                                    stock = self.fetchStock(str(sku))
                                    print(stock)
                                    desc = ''

                                    if stock != False:
                                        for key,value in stock.items():
                                            if 'GREEN' in str(value):
                                                desc = desc +':green_circle:US'+str(key) + '\n'
                                                
                                            if 'YELLOW' in str(value):
                                                desc = desc + ':yellow_circle:US'+str(key)+'\n'
                                                

                                    if stock != 'sold_out':
                                        self.send_webhook('footlocker-au',str(sku),str(title),str(link),'load',desc)
                                    else:
                                        self.send_webhook('footlocker-au',str(sku),str(title),str(link),'load',None)
                                        
                elif response.status_code == 503:
                    Main.fprint('Queue is live','yellow')
                    continue
                elif response.status_code != 200:
                    Main.fprint('Line 373 Error','red')
                    self.err('Failed connecting to footlocker [{}]'.format(str(response.status_code)))
            time.sleep(300)


    def getSku(self,link):
        sku = re.sub(r'^.*?v=', '', link)

        return sku

    def getTitle(self,link,sku):
        title = re.sub(r'^.*?/p/', '', link)
        title = title.replace('?v='+str(sku),'')
        title = title.replace('-',' ')
        title = title.title()

        return title

class Supplystore:
    def __init__(self):
        pass


class Sneakerboy:
    def __init__(self):
        pass


import discord 
from discord.ext import commands
Footlocker = Footlocker()

Thread(target=Footlocker).start()
#print(Footlocker.add_product('246780990904'))
#Footlocker.error('Failed connecting to footlocker')
#Footlocker.monitor()
#print(Footlocker.fetchStock('246780990904'))

Main.startDiscord('ODA3MjU0NzU3Njk3NTE5NjE2.YB1UlA.KPZUjtP7fFUHTH_q59zV4QGs-co')