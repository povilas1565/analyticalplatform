from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class Wallet(models.Model):
    """
        Wallet model

        address (TextField): address of Ethereum wallet,
        amount (FloatField): amount of currency in the wallet
    """

    address = models.TextField(verbose_name="Address", default="0x0")
    amount = models.FloatField(verbose_name="Amount", default=0.0)

    def __str__(self):
        return self.address


class Transaction(models.Model):
    """
        Transaction model

        id_external (TextField): address of transaction,
        amount (FloatField): transaction amount,
        price (FloatField): price in USDT,
        gas (FloatField): gas amount,
        gas_price (FloatField): gas price in USDT,
        created_on (DateTimeField): created at,
        from_wallet (ForeignKey Wallet): wallet from where the money was transferred,
        to_wallet (ForeignKey Wallet): wallet to the money was transferred,
        coin (ForeignKey Coin): coin
    """

    id_external = models.TextField(verbose_name="Transaction address", default="0x0")
    amount = models.FloatField(verbose_name="Amount", default=0.0)
    price = models.FloatField(verbose_name="Price in USDT", default=0.0)
    gas = models.FloatField(verbose_name="Gas amount", default=0.0)
    gas_price = models.FloatField(verbose_name="Gas price in USDT", default=0.0)
    created_on = models.DateTimeField(verbose_name="Created at", auto_now=True)
    commission = models.FloatField()
    from_wallet = models.ForeignKey(
        'analytics.Wallet',
        on_delete=models.CASCADE,
        related_name='from_wallet',
        verbose_name="Wallet from where the money was transferred"
    )
    to_wallet = models.ForeignKey(
        'analytics.Wallet',
        on_delete=models.CASCADE,
        related_name='to_wallet',
        verbose_name="Wallet to the money was transferred"
    )
    coin = models.ForeignKey(
        'analytics.Coin',
        on_delete=models.CASCADE,
        verbose_name="Transaction coin"
    )

    class Meta:
        indexes = [
            models.Index(fields=['created_on']),
        ]

    def __str__(self):
        return self.from_wallet.address


class Coin(models.Model):
    """
        Coin model

        title (CharField, Max length - 150): name of coin,
        image (FileField): icon of coin,
        ticker (CharField, Max length - 150): ticker of coin
        address (TextField): contract address,
        price (FloatField): price of coin in USDT,
        abi (TextField): ABI
    """

    title = models.CharField(verbose_name="Name of coin", max_length=150)
    image = models.FileField(verbose_name="Icon of coin", null=True)
    ticker = models.CharField(verbose_name="Ticker of coin", max_length=150)
    address = models.TextField(verbose_name="Contract address")
    price = models.FloatField(verbose_name="Price of coin in USDT", null=True, default=0.0)
    abi = models.TextField(verbose_name="ABI", null=True)

    def __str__(self):
        return self.title


class Whale(models.Model):
    """
        Proxy model to extend User abstract

        user (ForeignKey): abstract user,
        wallets (ManyToManyField, Wallet): tracked wallets,
        telegram (TextField): Telegram ID (not username)
    """

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, blank=True)
    wallets = models.ManyToManyField(Wallet, verbose_name='Tracked wallets', blank=True, null=True)
    telegram = models.TextField(default="durov", verbose_name='Telegram ID (not username)')


class WalletStat(models.Model):
    """
        WalletStat proxy statistic model

        address (TextField): address of Ethereum wallet,
        created_on (DateTimeField): statistics period,
        commission (FloatField): gas price in USDT,
        total_sell (FloatField): total buy amount by this wallet on period,
        total_buy (FloatField): total buy amount by this wallet on period,
        total_count_buy (IntegerField): buy transaction count on period,
        total_count_sell (IntegerField): sell transaction count on period,
        total_sell_price (FloatField): total sell amount by this wallet on period in USDT,
        total_buy_price (FloatField): total buy amount by this wallet on period in USDT
    """

    address = models.TextField(verbose_name='Address of Ethereum wallet', default="0x0", null=True)
    created_on = models.DateTimeField(verbose_name='Statistics period', null=True)
    commission = models.FloatField(verbose_name='Gas price in USDT', default=0.0, null=True)
    total_sell = models.FloatField(verbose_name='Total sell amount by this wallet on period', default=0.0, null=True)
    total_buy = models.FloatField(verbose_name='Total buy amount by this wallet on period', default=0.0, null=True)
    total_count_buy = models.IntegerField(verbose_name='Buy transaction count on period', default=0, null=True)
    total_count_sell = models.IntegerField(verbose_name='Sell transaction count on period', default=0, null=True)
    total_sell_price = models.FloatField(verbose_name='Total sell amount by this wallet on period in USDT', default=0.0, null=True)
    total_buy_price = models.FloatField(verbose_name='Total buy amount by this wallet on period in USDT', default=0.0, null=True)
    pnl_unrelease = models.FloatField(verbose_name='PNL unrelease', default=0.0, null=True)

    def __str__(self):
        return self.address


# User create signal
@receiver(post_save, sender=User)
def create_user_picks(sender, instance, created, **kwargs):
    if created:
        if not Whale.objects.filter(user=instance).exists():
            Whale.objects.create(user=instance)