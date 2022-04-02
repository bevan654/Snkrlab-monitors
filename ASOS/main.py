from utility import *
from termcolor import *
import colorama
from datetime import datetime
import json
import requests
import random
import time
from discord_webhook import DiscordWebhook, DiscordEmbed


proxies = Data().loadProxies('proxies.txt')
headers = {
    'cache-control':'DYNAMIC'
}
colorama.init()


class Task:
    def __init__(self,keyword):
        self.keyword = keyword
        self.products = []
        self.first_run = True

        self.start_monitor()


    def LOG(self,text,color='white'):
        print(colored(f"[{datetime.now()}][{self.keyword}] {text}",color))


    def sendWebhook(self,name,price,image,link):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/959351397546094663/jJ2Uz3kEGQkFLXT250orWt_34VcFuQOYLn7lb9FFR2-gSWJheQvDJGRnOO-KQdW6mTQD')

        embed = DiscordEmbed(title=name, description='``New Product``', url=link,color=15158332)
        embed.set_author(name='https://www.asos.com/au', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')
        embed.set_footer(text='Powered By Genesis | ASOS V1.0.0',icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')
        embed.set_thumbnail(url='https://'+image)
        embed.set_timestamp()
        embed.add_embed_field(name='PRICE', value=price)
        embed.add_embed_field(name='LINKS', value=f'[Product Link]({link})',inline=False)


        webhook.add_embed(embed)
        response = webhook.execute()


    def start_monitor(self):
        cycle = 0

        params = {
            'attribute_10992': '61388',
            'channel': 'mobile-web',
            'country': 'AU',
            'currency': 'AUD',
            'keyStoreDataversion': 'dup0qtf-35',
            'lang': 'en-AU',
            'limit': '72',
            'offset': '0',
            'q': self.keyword,
            'rowlength': '2',
            'store': 'AU',
            'z':str(random.randint(1,99999999999))
        }

        while True:
            cycle += 1


            if cycle == 1 or cycle == 2 or cycle % 500 == 1:
                self.LOG("Checking",'yellow')
            current_products = []
            try:
                response = requests.get('https://www.asos.com/api/product/search/v2/',params=params,proxies=random.choice(proxies),headers=headers)
            except:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue
            print(response.headers)

            if response.status_code == 200:
                try:
                    response = response.json()
                except:
                    self.LOG('Error Parsing JSON','red')
                    time.sleep(1)
                    continue

                
                for i in response['products']:
                    current_products.append(i['id'])
                    if i['id'] not in self.products:
                        self.products.append(i['id'])
                        if not self.first_run:
                            self.LOG("New Product! "+i['name'])
                            self.sendWebhook(i['name'],i['price']['current']['text'],i['imageUrl'],'https://www.asos.com/au/'+i['url'])
                    

                for k in self.products:
                    if k not in current_products:
                        self.LOG('Removed  product '+k,'red')
                        self.products.remove(k)

                





            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue
            self.first_run = False
            


Task('dunk')
