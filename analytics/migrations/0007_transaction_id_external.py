# Generated by Django 4.2.2 on 2023-07-01 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_alter_coin_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='id_external',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
