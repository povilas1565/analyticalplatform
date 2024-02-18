import json
from re import L
import time
import logging
import datetime
from _decimal import Decimal
from django.core.management.base import BaseCommand
from analytics.models import Transaction, Wallet, Coin, Whale
from crypto import settings
from web3 import Web3
import requests
import json
from django.db.models import Q
from django.conf import settings


web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))


def get_balance(address):
    balance_wei = web3.eth.get_balance(address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    return balance_eth


def get_abi(contract_address):
    if Coin.objects.filter(address=contract_address).exists():
        return Coin.objects.filter(address=contract_address).first()
    else:
        return False


def get_token_and_amount(tran):
    try:
        # Получаем объект транзакции
        transaction = tran

        # Получаем контрактный адрес (адрес токена, если это токеновая транзакция)
        contract_address = transaction.get('to', None)

        coin = Coin.objects.get_or_create(
            id=1
        )[0]

        # Если нет контрактного адреса, это обычная транзакция ETH
        if not contract_address:
            return [coin, web3.from_wei(transaction.get('value', 0), 'ether')]
        
        abi = get_abi(contract_address)
        if abi != False:
            # В противном случае это транзакция ERC20 токена
            # Загружаем контракт ERC20 по адресу
            contract = web3.eth.contract(address=contract_address, abi=json.loads(abi.abi))
            # Получаем адрес отправителя токена
            from_address = transaction.get('from', None)
            # Получаем количество токенов, которые были отправлены
            amount = contract.functions.balanceOf(from_address).call()
            # Возвращаем символ токена и объем
            return [abi, amount]
        else:
            return [coin, 0.0]

    except Exception as e:
        print(e)
        return None


def handle_transaction(tran):
    tx_hash = tran['hash'].hex()
    tx_from = tran['from']
    tx_to = tran['to']
    tx_value = web3.from_wei(tran['value'], 'ether')

    coin_first, status = Coin.objects.get_or_create(
        id=1
    )
    wallet_from = Wallet.objects.get_or_create(
        address = tran['from'],
        amount = get_balance(tran['from'])
    )
    wallet_to = Wallet.objects.get_or_create(
        address = tran['to'],
        amount = get_balance(tran['to'])
    )
    trans = get_token_and_amount(tran)
    if trans[1] == 0.0:
        trans[1] = tx_value
    transaction_created = Transaction.objects.create(
        from_wallet = wallet_from[0],
        to_wallet = wallet_to[0],
        id_external = tx_hash,
        amount=tx_value,
        commission=0.0,
        coin=trans[0],
        gas = 0.0,
        gas_price = 0.0,
        price=float(trans[1]) * trans[0].price
    )

    if Whale.objects.filter(Q(wallets__in=wallet_from[0]) | Q(wallets__in=wallet_to[0])).exists:
        for wh in Whale.objects.filter(Q(wallets__in=wallet_from[0]) | Q(wallets__in=wallet_to[0])):
            url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
            message_text = f"Кошелек {wallet_to[0].address} получил {tx_value} {trans[0].title} от {wallet_from[0].address} на сумму {float(trans[1]) * trans[0].price} $"
            params = {
                "chat_id": wh.telegram,
                "text": message_text,
            }
            requests.get(url, params=params)
            

    transaction_created.save()
    receipt = web3.eth.get_transaction_receipt(tx_hash)

    if receipt:
        tx_gas_price = web3.from_wei(tran['gasPrice'], 'gwei')
        tx_gas_used = receipt['gasUsed']
        tx_fee = web3.from_wei(tx_gas_price * tx_gas_used, 'ether')
        transaction_created.gas_price = float(tx_fee) * float(coin_first.price)
        transaction_created.gas = tx_fee
        transaction_created.save()
    print(f"Transaction {tx_hash} added")


def monitor_transactions():
    while True:
            latest_block_number = web3.eth.block_number
            try:
                latest_block = web3.eth.get_block(latest_block_number)
            except Exception as e:
                print(str(e))
            
            for tx_hash in latest_block['transactions']:
                transaction = web3.eth.get_transaction(tx_hash)
                try:
                    handle_transaction(transaction)
                except Exception as e:
                    print(str(e))

            latest_block_number += 1


class Command(BaseCommand):
    help = 'Scrape transactions from RPC node'

    def handle(self, *args, **kwargs):
        try:
            monitor_transactions()
        except:
            monitor_transactions()