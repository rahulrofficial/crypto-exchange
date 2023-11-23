from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
class User(AbstractUser):
    pass

class List_Coin(models.Model):
    coin_id=models.CharField(max_length=64,unique=True)
    symbol=models.CharField(max_length=16,unique=True)
    title=models.CharField(max_length=64,unique=True)
    logo_url=models.URLField(blank=True)
    #explorer=models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.symbol})"

class Coin(models.Model):
    coin=models.ForeignKey(List_Coin,on_delete=models.CASCADE,related_name="purchases")
    last_purchased=models.DateTimeField(default=datetime.datetime.now())
    current_coin_amount=models.FloatField(default=0)

    def __str__(self):
        return f"{self.coin} : {self.current_coin_amount}"

class Wallet(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="wallets")
    coins=models.ManyToManyField(Coin,blank=True,related_name="containing_wallets")

    def __str__(self):
        return f"{self.owner} has {[coin.coin.symbol for coin in self.coins.all()]}"

class Watchlist(models.Model):
    #user -foreign key
    watcher=models.ForeignKey(User,on_delete=models.CASCADE,related_name="watching")
    #itms
    watch_list=models.ManyToManyField(Coin,blank=True,related_name="watchers")

class History(models.Model):
    transaction_on=models.DateTimeField(default=datetime.datetime.now())
    buyer_receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="received")
    seller_sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="send")
    transacted_coin=models.ForeignKey(List_Coin,on_delete=models.CASCADE,related_name="transacted")
    transacted_coin_value=models.FloatField()
    transacted_amount=models.FloatField(default=0)

    def __str__(self):
        return f"{self.seller_sender} send/sold {self.transacted_amount} {self.transacted_coin} at {self.transacted_coin_value} per USD to {self.buyer_receiver} on {self.transaction_on.strftime('%c')}"