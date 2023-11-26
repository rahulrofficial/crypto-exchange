# Generated by Django 4.2.6 on 2023-11-25 14:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0022_alter_coin_last_purchased_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='last_purchased',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 19, 40, 27, 389548)),
        ),
        migrations.AlterField(
            model_name='history',
            name='transaction_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 19, 40, 27, 405169)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 19, 40, 27, 405169)),
        ),
    ]
