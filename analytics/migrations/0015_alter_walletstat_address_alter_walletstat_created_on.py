# Generated by Django 4.2.2 on 2023-07-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0014_alter_walletstat_commission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletstat',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='walletstat',
            name='created_on',
            field=models.DateTimeField(null=True),
        ),
    ]