# Generated by Django 4.2.6 on 2023-11-23 17:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0010_alter_coin_last_purchased_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='last_purchased',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 23, 2, 8, 553450)),
        ),
        migrations.AlterField(
            model_name='history',
            name='transaction_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 23, 2, 8, 553450)),
        ),
        migrations.CreateModel(
            name='Order_wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frozen_amount', models.FloatField(default=0)),
                ('lister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_wallet', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_orders', to='exchange.orders')),
                ('temp_coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='running', to='exchange.list_coin')),
            ],
        ),
    ]
