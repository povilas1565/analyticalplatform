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


def get_ethusdt_price():
    response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT')
    data = response.json()
    price = float(data['price'])
    return price

def update_ethusdt_price():
    while True:
        price = get_ethusdt_price()
        coin = Coin.objects.get_or_create(
            id=1
        )
        coin = coin[0]
        coin.price = price
        coin.save()
        print(f"ETHUSDT price: {price}")
        time.sleep(30)


class Command(BaseCommand):
    help = 'Scrape data about Etherium price'

    def handle(self, *args, **kwargs):
        update_ethusdt_price()