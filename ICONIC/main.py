import requests
import threading
import colorama
from termcolor import *
from utility import *
from datetime import *
import time

import random
from discord_webhook import DiscordWebhook, DiscordEmbed

colorama.init()

proxies = Data().loadProxies('proxies.txt')
screen_lock = threading.Semaphore(value=1)
keywords = ['550','2002r']


headers = {
    'Cache-Control':'max-age=0'
}


class Monitor:
    def __init__(self,keyword):
        self.keyword = keyword
        self.first_run = True

        self.skus = []
        self.LOG("[INITAL] Retrieving Products!",'magenta')
        self.start_monitor()


    def send_webhook(self,sku,price,name,slug):
        webhook = 'https://discord.com/api/webhooks/967674220060487710/TUCg1V11k4OExyOHOAGdUapAa45Q91LexMULJUCYsyK6qhPVvJzewzPm06MJ3NoO-WkA'
        webhook = DiscordWebhook(url=webhook)

        embed = DiscordEmbed(title=name, color=15158332,url='https://www.theiconic.com.au/'+slug+'?category=slot')

        embed.set_author(name='https://www.theiconic.com.au',icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')



        embed.set_footer(text='Genesis x Toyu | ICONIC V1.0.0', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')


        embed.set_timestamp()

        embed.add_embed_field(name='PRICE', value=str(price))
        embed.add_embed_field(name='SKU', value=str(sku))

        webhook.add_embed(embed)

        response = webhook.execute()


    def LOG(self,text,color='white'):
        try:
            screen_lock.acquire()
            print(colored(f'[{datetime.now()}][{self.keyword}] {text}',color))
            screen_lock.release()
        except Exception as e:
            print(e)
            print(text)

    def start_monitor(self):
        self.cycle = 0
        while True:
            self.cycle += 1


            if self.cycle == 2 or self.cycle == 3 or self.cycle % 500 == 0:
                self.LOG('[MONITOR] Watching for restocks...','magenta')

            try:
                response = requests.get(f'https://eve.theiconic.com.au/v2/catalog/products?q={self.keyword}&sort=new',headers=headers,proxies=random.choice(proxies))
            except Exception as e:
                print(e)
                self.LOG("[MONITOR] Request Error",'red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                try:
                    response = response.json()
                except:
                    self.LOG("[MONITOR] Error Loading JSON",'red')
                    time.sleep(1)
                    continue

                new_skus = []
                for i in response['_embedded']['product']:
                    new_skus.append(i['sku'])
                    if i['sku'] not in self.skus:
                        self.skus.append(i['sku'])
                        if 'shoes' in i['categories_translated'].lower() or 'shoe' in i['categories_translated'].lower():
                            if not self.first_run:
                                self.LOG("[NEW PRODUCT] "+i['name'],'green')
                                self.send_webhook(i['sku'],str(i['price']),str(i['name']),str(i['link']))


                for i in self.skus:
                    if i not in new_skus:
                        self.skus.remove(i)

                if self.first_run:
                    self.LOG("[INTIAL] Starting monitor...",'yellow')
                    self.first_run = False
            elif response.status_code == 403:
                self.LOG("[MONITOR] 403 Unauthorized Access",'red')
                time.sleep(1)
                continue

            else:
                self.LOG('Bad Response Status '+str(response.status_code),'red')
                time.sleep(1)
                continue

def main():
    for i in keywords:
        threading.Thread(target=Monitor,args=(i,)).start()


main()
