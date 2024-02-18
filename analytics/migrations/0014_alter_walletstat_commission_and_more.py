# Generated by Django 4.2.2 on 2023-07-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0013_alter_walletstat_commission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletstat',
            name='commission',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='total_buy',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='total_buy_price',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='total_count_buy',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='total_count_sell',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='total_sell',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='total_sell_price',
            field=models.IntegerField(default=0, null=True),
        ),
    ]