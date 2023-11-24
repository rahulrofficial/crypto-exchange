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
    #items
    watch_list=models.ManyToManyField(List_Coin,blank=True,related_name="watchers")

class History(models.Model):
    transaction_on=models.DateTimeField(default=datetime.datetime.now())
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="received")
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="send")
    transacted_coin=models.ForeignKey(List_Coin,on_delete=models.CASCADE,related_name="transacted")
    transacted_coin_value=models.FloatField()
    """transacted_amount-number of coins
    """
    transacted_amount=models.FloatField(default=0)#number of coins
    transact_action=models.CharField(max_length=64,blank=True)#Purchased/Sold/Send/

    def __str__(self):
        return f"{self.from_user} {self.transact_action} {self.transacted_amount} {self.transacted_coin} at {self.transacted_coin_value} per USD to {self.to_user} on {self.transaction_on.strftime('%c')}"
    
    
class Orders(models.Model):
    lister=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    order_coin=models.ForeignKey(List_Coin,on_delete=models.CASCADE,related_name="listed")
    order_coin_no=models.FloatField()
    order_price_per_coin=models.FloatField()# required amount/coin
    order_amount=models.FloatField(default=0) #total amount required to fulfill the order
    is_buy=models.BooleanField(default=True)
    created=models.DateTimeField(default=datetime.datetime.now())
    is_fulfilled=models.BooleanField(default=False)
    fulfilled_on=models.DateTimeField(null=True)
    is_closed=models.BooleanField(default=False)#is lister closed the order    
    closed_on=models.DateTimeField(null=True)
    
    
    def __str__(self):
        action="Buy" if self.is_buy else "Sell"
        return f"{self.lister} wanted to {action} {self.order_coin_no} {self.order_coin} at ${self.order_price_per_coin}/coin"
    
class Order_wallet(models.Model):
    lister=models.ForeignKey(User,on_delete=models.CASCADE,related_name="temp_wallet")
    order=models.ForeignKey(Orders,on_delete=models.CASCADE,related_name="active_orders")
    temp_coin=models.ForeignKey(List_Coin,on_delete=models.CASCADE,related_name="running")
    frozen_amount=models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.lister}'s {self.frozen_amount} {self.temp_coin} are temporary unavailable until order is closed/Fulfilled"
    
    
    
    