from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Count, F, Sum, Q #, FloatField, ExpressionWrapper, Case, When
from django.db.models.functions import Round
from .models import Wallet, Coin, Transaction, WalletStat, Whale
from django.db import connection


class AnalyticsView(View):
    """
        Render template to statistics by profit.

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (template): 'analytics/home.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/home.html',
                {
                    'css': "css/login.css",
                    "from_date": request.GET.get('from-date', '2015-01-01'),
                    "to_date": request.GET.get('to-date', '2025-01-01')
                }
            )
        return HttpResponseRedirect('/login')


class AnalyticsJsonView(View):
    """
        Return JSON to statistics by profit.

        Models:
            analytics.WalletStat

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (JSON)
    """

    def get(self, request, *args, **kwargs):
        wallets = WalletStat.objects.filter(
            total_count_buy__gt = 0,
            total_count_sell__gt = 0,
            created_on__range = (request.GET.get('from-date', '2015-01-01'), request.GET.get('to-date', '2025-07-01'))
        ).values().order_by("-address").annotate(
            pnl_release = ((F("total_buy_price") / F("total_buy")) * F("total_sell"))- F("total_buy_price"),
            diff_buysell = F("total_sell") - F("total_buy"),
            total_count = F("total_count_buy") + F("total_count_sell")
        ).filter(
            pnl_release__gt=0
        ).annotate(
            pnl_percent = (F("pnl_release") * 100) / Sum("total_buy_price"),
            winrate = (Round(((F("total_count_buy"))/2)-1) * 100) / F("total_count_buy")
        ).filter(
            pnl_percent__lte = 150
        ).order_by("-winrate","-pnl_release")

        return JsonResponse({"qs": list(wallets)}, safe=False)


class SuccessView(View):
    """
        Render template to statistics by success.

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (template): 'analytics/success.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/success.html',
                {
                    'css': "css/login.css",
                    "from_date": request.GET.get('from-date', '2015-01-01'),
                    "to_date": request.GET.get('to-date', '2025-01-01')
                }
            )
        return HttpResponseRedirect('/login')


class SuccessJsonView(View):
    """
        Return JSON to statistics by success.

        Models:
            analytics.WalletStat

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (JSON)
    """

    def get(self, request, *args, **kwargs):
        wallets = WalletStat.objects.filter(
            total_count_buy__gt = 0,
            total_count_sell__gt = 0,
            created_on__range = (request.GET.get('from-date', '2015-01-01'), request.GET.get('to-date', '2025-07-01'))
        ).values().order_by("-address").annotate(
            pnl_release = ((F("total_buy_price") / F("total_buy")) * F("total_sell"))- F("total_buy_price"),
            diff_buysell = F("total_sell") - F("total_buy"),
            total_count = F("total_count_buy") + F("total_count_sell")
        ).filter(
            pnl_release__gt=0
        ).annotate(
            pnl_percent = (F("pnl_release") * 100) / Sum("total_buy_price"),
            winrate = (Round(((F("total_count_buy"))/2)-1) * 100) / F("total_count_buy")
        ).filter(
            pnl_percent__lte = 150
        ).order_by("-pnl_release","-winrate")
        return JsonResponse({"qs": list(wallets)}, safe=False)


class WinrateView(View):
    """
        Render template to statistics by winrate.

        Models:
            analytics.Wallet

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (template): 'analytics/winrate.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/winrate.html',
                {
                    'css': "css/login.css",
                    "from_date": request.GET.get('from-date', '2015-01-01'),
                    "to_date": request.GET.get('to-date', '2025-01-01')
                }
            )
        return HttpResponseRedirect('/login')


class WinrateJsonView(View):
    """
        Return JSON to statistics by winrate.

        Models:
            analytics.WalletStat

        Accept (GET):
            winrate (string): "10-100",
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (JSON)
    """

    def get(self, request, *args, **kwargs):
        params_winrate = {
            "winrate__gte": 10,
            "winrate__lte": 100
        }
        winrate = request.GET.get('winrate','')
        if len(winrate) > 0 and len(winrate.split("-")) > 0:
            params_winrate["winrate__gte"] = int(winrate.split("-")[0])
            params_winrate["winrate__lte"] = int(winrate.split("-")[1])
        wallets = WalletStat.objects.filter(
            total_count_buy__gt = 0,
            total_count_sell__gt = 0,
            created_on__range = (request.GET.get('from-date', '2015-01-01'), request.GET.get('to-date', '2025-07-01'))
        ).values().order_by("-address").annotate(
            pnl_release = ((F("total_buy_price") / F("total_buy")) * F("total_sell"))- F("total_buy_price"),
            diff_buysell = F("total_sell") - F("total_buy"),
            total_count = F("total_count_buy") + F("total_count_sell")
        ).filter(
            pnl_release__gt=0
        ).annotate(
            pnl_percent = (F("pnl_release") * 100) / Sum("total_buy_price"),
            winrate = (Round(((F("total_count_buy"))/2)-1) * 100) / F("total_count_buy")
        ).filter(
            pnl_percent__lte = 150, **params_winrate
        ).order_by("-winrate","-pnl_release")
        return JsonResponse({"qs": list(wallets)}, safe=False)


class CoinRatingView(View):
    """
        Render template to list of coins.

        Models:
            analytics.Coin

        Response (template): 'analytics/coin_rating.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/coin_rating.html',
                {
                    'css': "css/login.css",
                    'coins': Coin.objects.all().annotate(transactions_count=Count("transaction", distinct=True)).order_by("-transactions_count")
                }
            )
        return HttpResponseRedirect('/login')


class CoinRatingItemView(View):
    """
        Render template to transaction statistics by coin.

        Models:
            analytics.Coin

        Response (template): 'analytics/coin_rating_item.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            coin_getted = get_object_or_404(Coin, id=self.kwargs["id"])
            return render(
                request,
                'analytics/coin_rating_item.html',
                {
                    'css': "css/login.css",
                    'coin': coin_getted
                }
            )
        return HttpResponseRedirect('/login')


class CoinRatingItemJsonView(View):
    """
        Return JSON to transaction statistics by coin.

        Models:
            analytics.Wallet

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (JSON)
    """

    def get(self, request, *args, **kwargs):
        wallets = Wallet.objects.filter(
            from_wallet__coin__id = self.kwargs["id"],
            from_wallet__created_on__range = (request.GET.get('from-date', '2015-01-01'), request.GET.get('to-date', '2025-07-01'))
        ).annotate(amount_tran=Sum(F("from_wallet__amount"))).order_by("-amount_tran", "address").values("address", "amount_tran")
        return JsonResponse({"qs": list(wallets)}, safe=False)


class TransactionView(View):
    """
        Render template of coin list to transaction statistics.

        Models:
            analytics.Coin

        Response (template): 'analytics/transaction.html'
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/transaction.html',
                {
                    "css": "css/login.css",
                    "coins": Coin.objects.all().annotate(
                        transactions_count=Count("transaction", distinct=True)
                    ).order_by("-transactions_count")
                }
            )
        return HttpResponseRedirect('/login')


class TransactionItemView(View):
    """
        Render template to transaction statistics.

        Models:
            analytics.Coin

        Response (template): 'analytics/transactionitem.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            coin_getted = get_object_or_404(Coin, id=self.kwargs["id"])
            return render(
                request,
                'analytics/transactionitem.html',
                {
                    'css': "css/login.css",
                    'coin': coin_getted
                }
            )
        return HttpResponseRedirect('/login')


class TransactionJsonView(View):
    """
        Return JSON to transaction statistics by coin.

        Models:
            analytics.Wallet

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (JSON)
    """

    def get(self, request, *args, **kwargs):
        wallets = Transaction.objects.filter(
            coin__id = self.kwargs["id"],
            created_on__range = (request.GET.get('from-date', '2015-01-01'), request.GET.get('to-date', '2025-07-01'))
        ).values()
        return JsonResponse({"qs": list(wallets)}, safe=False)


class WalletView(View):
    """
        Render template to wallets list and subscribe to wallet (POST).

        Models:
            analytics.Coin

        Accept (POST):
            address (string): "0x0"

        Response (template): 'analytics/wallets.html'
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/wallets.html',
                {
                    'css': "css/login.css",
                    'wallets': Wallet.objects.all(),
                    'whale': Whale.objects.filter(user=request.user)[0]
                }
            )
        return HttpResponseRedirect('/login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            whale_user = Whale.objects.filter(user=request.user)[0]
            wall = Wallet.objects.get_or_create(
                address = request.POST.get('address',''),
                amount = 0.0
            )[0]
            whale_user.wallets.add(wall)
            whale_user.save()
            return HttpResponseRedirect('/wallet/')
        return HttpResponseRedirect('/login')


class WalletItemView(View):
    """
        Render template to transaction statistics by wallet.

        Models:
            analytics.Wallet

        Accept (kwarg):
            id (int): 1

        Response (template): 'analytics/wallets_item.html'
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                'analytics/wallets_item.html',
                {
                    'css': "css/login.css",
                    'wallets': Wallet.objects.get(id=self.kwargs['id']),
                    "from_date": request.GET.get('from-date','2015-01-01'),
                    "to_date": request.GET.get('to-date','')
                }
            )
        return HttpResponseRedirect('/login')


class WalletJsonView(View):
    """
        Return JSON to transaction statistics by wallet.

        Models:
            analytics.Coin

        Accept (kwarg):
            id (int): 1

        Accept (GET):
            from-date (date): "2015-01-01",
            to-date (date): "2025-07-01"

        Response (JSON)
    """

    def get(self, request, *args, **kwargs):
        wallets = Transaction.objects.filter(
            Q(from_wallet__id = self.kwargs['id']) | Q(self.kwargs['id']),
            created_on__range = (request.GET.get('from-date', '2015-01-01'), request.GET.get('to-date', '2025-07-01'))
        ).values()
        return JsonResponse({"qs": list(wallets)}, safe=False)
