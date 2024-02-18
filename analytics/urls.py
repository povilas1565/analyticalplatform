from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import AnalyticsView, WinrateView, SuccessView, CoinRatingView, TransactionView, WalletView, \
    CoinRatingItemView, TransactionItemView, AnalyticsJsonView, WalletJsonView, WinrateJsonView, SuccessJsonView, WalletItemView, CoinRatingItemJsonView, TransactionJsonView

urlpatterns = [
    path('', AnalyticsView.as_view(), name='profit'),
    path('api/v1/profit/json/', AnalyticsJsonView.as_view(), name='profitjson'),
    path('api/v1/success/json/', SuccessJsonView.as_view(), name='profitjson'),
    path('api/v1/winrate/json/', WinrateJsonView.as_view(), name='profitjson'),
    path('api/v1/wallet/json/<id>/', WalletJsonView.as_view(), name='profitjson'),
    path('api/v1/coin/json/<id>/', CoinRatingItemJsonView.as_view(), name='profitjson'),
    path('api/v1/transaction/json/<id>/', TransactionJsonView.as_view(), name='profitjson'),
    path('success/', SuccessView.as_view(), name='success'),
    path('winrate/', WinrateView.as_view(), name='winrate'),
    path('coinrating/', CoinRatingView.as_view(), name='coinrating'),
    path('coinrating/<id>/', CoinRatingItemView.as_view(), name='coinrating'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('transaction/<id>/', TransactionItemView.as_view(), name='coinrating'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/<id>/', WalletItemView.as_view(), name='wallet')
]