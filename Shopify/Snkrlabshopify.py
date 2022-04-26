import requests
import colorama
from utility import *
from termcolor import *
import datetime
import time
import json
import pyperclip
from discord_webhook import *
import random
import threading
colorama.init()
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("SNKRLab Shopify")
class Shopify:
    def __init__(self):
        self.first_run = True
        self.products = []
        self.proxies = Data().loadProxies('proxies.txt')
        self.sites = [
            "https://laced.com.au/collections/jordan",
            "https://laced.com.au/collections/nike",
            "https://laced.com.au/collections/new-balance",
            "https://www.finessestore.com/collections/nike",
            "https://www.finessestore.com/collections/jordan",
            "https://www.finessestore.com/collections/new-balance",
            "https://www.culturekings.com.au/collections/jordan",
            "https://www.culturekings.com.au/collections/nike",
            "https://uptherestore.com/collections/jordan",
            "https://uptherestore.com/collections/nike",
            "https://uptherestore.com/collections/new-balance",
            "https://www.highsandlows.net.au/collections/nike",
            "https://www.highsandlows.net.au/collections/new-balance",
            "https://www.abovethecloudsstore.com/collections/nike",
            "https://www.abovethecloudsstore.com/collections/nike-sb",
            "https://www.abovethecloudsstore.com/collections/new-balance",
            "https://www.abovethecloudsstore.com/collections/jordan-brand",
            "https://www.incu.com/collections/new-balance",
            "https://www.incu.com/collections/nike",
            "https://usgstore.com.au/collections/jordan",
            "https://usgstore.com.au/collections/nike",
            "https://50-50.com.au/collections/new-balance-shoes",
            "https://50-50.com.au/collections/nike-sb-skate-shoes",
            "https://www.empireskate.co.nz/collections/nike",
            "https://www.empireskate.co.nz/collections/new-balance",
            "https://www.empireskate.co.nz/collections/new-balance-numeric",
            "https://shop.goodasgoldshop.com/collections/nike",
            "https://shop.goodasgoldshop.com/collections/new-balance",
            "https://www.wearedropouts.com.au/collections/nike-sb",
            "https://usgstore.com.au/collections/nike",
            "https://www.hoopsheaven.com.au/collections/jordan",
            "https://www.hoopsheaven.com.au/collections/nike",
            "https://upsskateshop.com.au/collections/nike-sb",
            "https://upsskateshop.com.au/collections/new-balance-numeric",
            "https://www.k101store.com/collections/kickz",
            "https://area51store.co.nz/collections/nike",
            "https://antisocialcollective.com/collections/nike-sb-footwear",
            "https://shop.ccs.com/collections/nike-sb",
            "https://shop.ccs.com/collections/new-balance",
            "https://www.ocdskateshop.com.au/collections/nike-sb",
            "https://1991skateshop.com.au/collections/nike-sb",
            "https://shop.doverstreetmarket.com/collections/shops-nikelab-dsm",
            "https://limitededt.com/collections/new-balance",
            "https://limitededt.com/collections/new-balance-made",
            "https://limitededt.com/collections/nike",
            "https://limitededt.com/collections/nikelab"

        ]
        self.in_stock = {}
        self.run_number = 0
    def LOG(self, stats, text, color):
        print(colored(f"[{datetime.datetime.now()}] [{stats}] {text}", color))
    
    def update_status(self, site="None"):
        ctypes.windll.kernel32.SetConsoleTitleW(f"SNKRLab Shopify | Checking: {site} | Run: {str(self.run_number)}")
    def alert(self, title, url, image_url, sizes):
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/901275359859834920/x7FsuOvsfudRPWkkwLpei9uhzR-uY0fCtXZd0N0NafW4DO-0nAaMKg1v4DNje6jgcuze")
        embed = DiscordEmbed(title=str(title), color="00FF00", url=url)
        embed.add_embed_field(name="**Sizes**", value="".join(sizes), inline=False)
        embed.set_timestamp()
        embed.set_thumbnail(url=image_url)
        embed.set_footer(text="SNKRLab Shopify | Coded by Toyu | V1.0.0")
        webhook.add_embed(embed)
        try:
            webhook.execute()
        except Exception as e:
            print(e)
            print(title)
            print(url)
            print(image_url)
            print(sizes)

    def pick_proxy(self):
        proxies = random.choice(self.proxies)
        return proxies

    def check_stock(self, site):
        self.update_status(site)
        keywords = [
            "jordan 1",
            "jordan 2",
            "jordan 3", 
            "jordan 4", 
            "jordan 5", 
            "jordan 6", 
            "jordan 9", 
            "jordan 10", 
            "jordan 11", 
            "jordan 12", 
            "jordan 13", 
            "yeezy", 
            "dunk",
            "2002r",
            "550"
        ]

        site_stripped = site.split("/")
        site_stripped = "https://"+site_stripped[2]
        try:
            headers = {
                'method': 'GET',
                'scheme': 'https',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
            }
            r = requests.get(site+"/products.json?limit=300", headers=headers, timeout=10, proxies=self.pick_proxy())
        except Exception as e:
            self.LOG("REQUESTS", "Failed to get Site.... Error {}".format(e), "red")
            time.sleep(5)
            return
        
        if r.status_code == 200:
            try:
                json_data = json.loads(r.text)
            except:
                self.LOG("JSON", "Failed to create JSON....", "red")
                time.sleep(5)
                return

            current_stock = []
            for product in json_data["products"]:
                sizes = []
                current_stock.append(product["id"])
                if product['id'] not in self.in_stock.keys():
                    self.in_stock.update({product['id']:site})
                    if self.first_run == False:
                        self.LOG("CHECKER", f"New Product! Name: {product['title']}", "green")
                        for variant in product["variants"]:
                            if variant["available"] == True:
                                sizes.append(f'{variant["title"]} | **[ATC]({site_stripped}/cart/{variant["id"]}:1)**\n')
                        if sizes:
                            self.alert(product["title"], f"{site_stripped}/products/"+product["handle"], product["images"][0]["src"], sizes)
                            pass
            for product in self.in_stock.keys():
                if product not in current_stock:
                    if self.in_stock[product] == site:
                        self.LOG("PRODUCT", "Removed product: "+str(product),'red')
                        self.in_stock.pop(product)

        else:
            self.LOG("REQUESTS", f"Failed to get site: {site} | Text: {r.content} | Response: {str(r.status_code)}", "red")
            time.sleep(10)
            return
                
    def monitor(self):
        while True:
            self.run_number += 1
            start = time.time()
            self.LOG("CHECKER", "Checking Stock...", "yellow")
            threads = []
            for site in self.sites:
                self.check_stock(site)
            self.first_run = False
            finish = time.time()

            self.LOG("CHECKER", f"No Stock! Run Time: {str(round(finish - start))}s", "red")
            current = ",".join(str(i) for i in self.in_stock)
            pyperclip.copy(current)

Shopify().monitor()