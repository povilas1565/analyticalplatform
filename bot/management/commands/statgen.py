import datetime
from django.core.management.base import BaseCommand
from analytics.models import WalletStat
from django.db import connection
from crypto import settings


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]


def stategen():
    cursor = connection.cursor()
    wallets = cursor.execute(f'''
        SELECT
            res.address,
            res.created_on,
            res.amount,
            res.commission,
            res.total_sell,
            res.total_buy,
            res.total_spent,
            res.total_count_buy,
            res.total_count_sell,
            res.total_sell_price,
            res.total_buy_price,
            res.pnl_unrelease
        FROM (
            SELECT
                w."address",
                SUM(w."amount") AS "pnl_unrelease",
                date_trunc('day', COALESCE(t1."created_on", t2."created_on")) AS "created_on",
                SUM(t1."price") + SUM(t2."price") as "amount",
                SUM(COALESCE(t1."gas_price", 0) + COALESCE(t2."gas_price", 0)) AS "commission",
                SUM(t1."amount") AS "total_sell",
                SUM(t2."amount") AS "total_buy",
                (SUM(t2."price") - SUM(t1."price")) AS "total_spent",
                COUNT(DISTINCT t2."id") AS "total_count_buy",
                COUNT(DISTINCT t1."id") AS "total_count_sell",
                SUM(t1."price") AS "total_sell_price",
                SUM(t2."price") AS "total_buy_price"
            FROM
                "analytics_wallet" w
            LEFT OUTER JOIN
                "analytics_transaction" t1 ON (w."id" = t1."from_wallet_id" AND t1."amount" > 0.1)
            LEFT OUTER JOIN
                "analytics_transaction" t2 ON (w."id" = t2."to_wallet_id" AND t2."amount" > 0.1)
            GROUP BY
                date_trunc('day', COALESCE(t1."created_on", t2."created_on")),
                w."address"
            HAVING
                COUNT(t2."id") < 50 AND COUNT(t1."id") < 50
        ) res;
    ''')
    qs_json = dictfetchall(cursor)
    for i, qc in enumerate(qs_json):
        print(f"Stat generate = {i}/{len(qs_json)}")
        obj, created = WalletStat.objects.get_or_create(
            address = qc["address"] if "address" in qc else 0,
            created_on = qc["created_on"] if "created_on" in qc else 0
        )
        obj.commission = str(qc["commission"] if qc["commission"] != None else 0)[0:5]
        obj.total_sell = round(qc["total_sell"] if qc["total_sell"] != None else 0, 2)
        obj.total_buy = round(qc["total_buy"] if qc["total_buy"] != None else 0, 2)
        obj.total_count_buy = round(qc["total_count_buy"] if qc["total_count_buy"] != None else 0, 2)
        obj.total_count_sell = round(qc["total_count_sell"] if qc["total_count_sell"] != None else 0, 2)
        obj.total_sell_price = round(qc["total_sell_price"] if qc["total_sell_price"] != None else 0, 2)
        obj.total_buy_price = round(qc["total_buy_price"] if qc["total_buy_price"] != None else 0, 2)
        obj.pnl_unrelease = qc["pnl_unrelease"] if qc["pnl_unrelease"] != None else 0.0
        obj.save()


class Command(BaseCommand):
    help = 'Generate stat from your transaction Django model'

    def handle(self, *args, **kwargs):
        stategen()