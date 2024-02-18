import json
import time
import logging
import datetime
import requests
from django.core.management.base import BaseCommand
from analytics.models import Transaction, Wallet, Coin
from bs4 import BeautifulSoup
import requests
import json
import time
import cloudscraper
from django.db import models
from crypto import settings


def updater_coin():
    proxies = {
        "http": "socks5://z7xXnMjC:P3Jb8v3p@45.153.224.10:61787",
        "https": "socks5://z7xXnMjC:P3Jb8v3p@45.143.142.50:62327"
    }
    coins = []
    scraper = cloudscraper.create_scraper()
    for page in list(range(1, 14)):
        url = f"https://api.ipify.org"
        soup = BeautifulSoup(scraper.get(url, proxies=proxies).text)
        print(soup.prettify())
        url = f"https://etherscan.io/tokens?ps=100&p={page}"
        soup = BeautifulSoup(scraper.get(url, proxies=proxies).text)
        print(soup.prettify())
        table = soup.find("tbody")
        rows = table.findAll("tr")
        for row in rows:
            rowrow = row.findAllNext("td")
            address = rowrow[1].findNext("a")["href"].replace("/token/", "")
            title = rowrow[1].text.replace("\n", "").split("(")[0]
            ticker = rowrow[1].text.replace("\n", "").split("(")[1].replace(")", "")
            price = float(rowrow[2].findNext("div").text.replace("\n", "").replace("$", "").replace(",", ""))
            coin, status = Coin.objects.get_or_create(
                title=str(title.replace("’", "").replace("智投链", "IIC")),
                ticker=str(ticker),
                address=str(address)
            )
            coin.price=price
            url = f"https://api.etherscan.io/api?module=contract&action=getabi&address=0xdac17f958d2ee523a2206206994597c13d831ec7&apikey=1ZSXE1MN1I8ZQUDR77E772FBCAURV8B26E"
            coin.abi = json.dumps(requests.get(
                    url=url
            ).json()["result"])
            coin.save()
        time.sleep(3)


class Command(BaseCommand):
    help = 'Scrape data about tokens price'

    def handle(self, *args, **kwargs):
        updater_coin()