import colorama
from utility import *
from datetime import datetime
import json
import requests
import random
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from termcolor import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = Data().loadProxies('proxies.txt')

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'cache-control':'max-age=0'
}
colorama.init()


screen_lock = threading.Semaphore(value=1)


class Task:
    def __init__(self,keyword):
        self.keyword = keyword
        self.products = []
        self.first_run = True

        self.start_monitor()

    def LOG(self,text,color='white'):
        try:
            screen_lock.acquire()
            print(colored(f"[{datetime.now()}][{self.keyword}] {text}",color))
            screen_lock.release()
        except:
            print(colored(f"[{datetime.now()}][{self.keyword}] {text}",color))



    def sendWebhook(self,name,price,image,link):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/959694423799763005/Ir2hk2MNYbzRTPtfia4zCaaKi6uHydSjLR8Ss72Q-KRt4890eIY0q1Q_sug8z2FIA9Fz')
        embed = DiscordEmbed(title=name, description='``New Product``', url=link,color=15158332)
        embed.set_author(name='https://www.asos.com/au', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')
        embed.set_footer(text='Powered By Genesis | Code by Toyu | ASOS V1.0.0',icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')
        embed.set_thumbnail(url='https://'+image)
        embed.set_timestamp()
        embed.add_embed_field(name='**Price**', value=price)
        webhook.add_embed(embed)
        webhook.execute()


    def start_monitor(self):
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
            current_products = []
            self.LOG("Checking Stock...",'yellow')
            
            #Create Request
            try:
                r = requests.get('https://www.asos.com/api/product/search/v2/',params=params, proxies=random.choice(proxies), headers=headers)
            except Exception as e:
                print(e)
                self.LOG("Bad Response Status",'red')
                time.sleep(10)
                continue
            #Create JSON
            if r.status_code == 200:
                try:
                    json_data = json.loads(r.text)
                except:
                    self.LOG("Failed to Create JSON", "red")
                    time.sleep(10)
                    continue

                #Check Items
                for i in json_data['products']:
                    current_products.append(i['id'])
                    if i['id'] not in self.products:
                        self.products.append(i['id'])
                        if self.first_run == False:
                            self.LOG("New Product! "+i['name'])
                            self.sendWebhook(i['name'],i['price']['current']['text'],i['imageUrl'],'https://www.asos.com/au/'+i['url'])

                #Check for OOS Items then Remove
                for k in self.products:
                    if k not in current_products:
                        self.LOG('Removed product '+k,'red')
                        self.products.remove(k)

            else:
                self.LOG("Bad Response Status: "+str(r.status_code),'red')
                time.sleep(10)
                continue

            self.first_run = False
            time.sleep(10)
    


keywords = ['dunk','jordan']


for i in keywords:
    threading.Thread(target=Task,args=(i,)).start()