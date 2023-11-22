from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import User,List_Coin,Coin,Wallet,Watchlist,History
from django import forms
import requests
import json




def database_listed_coins_updater():
    
    if not len(List_Coin.objects.all()):
        coin=List_Coin(
            coin_id='usd',
            symbol='USD',
            title='US Dollar',
            logo_url='https://cdn.pixabay.com/photo/2016/01/25/01/52/dollar-1159943_1280.png'
        )
        coin.save()
        url = 'https://api.coincap.io/v2/assets'    
        res = requests.get(url)
        response = json.loads(res.text)
        for item in response['data']:
            print(item['id'])
            coins=List_Coin(
            coin_id=item['id'],
            symbol=item['symbol'],
            title=item['name'],
            logo_url=f"https://cryptologos.cc/logos/{item['id']}-{item['symbol'].lower()}-logo.png"
                            )
            coins.save()
            
        print('Coins Updated Successfully')
database_listed_coins_updater()
def is_user(username):
    if not username in [user.username for user in User.objects.all()]:
        raise ValidationError

class Deposit(forms.Form):
    amount=forms.IntegerField(label=False,required=True,widget=forms.NumberInput(attrs={"class": "form-control w-75",'placeholder':'Deposit'}))

class Buy_Sell(forms.Form):
    coin_list=tuple((coin.id,coin.title) for coin in List_Coin.objects.all())
    
    
    coins=forms.ChoiceField(label=False,choices=coin_list,required=True,widget=forms.Select(attrs={"class": "form-control w-75"})) 
    amount=forms.FloatField(label=False,required=True,widget=forms.NumberInput(attrs={"class": "form-control w-75",'placeholder':'Amount'}))
    action=forms.ChoiceField(widget=forms.RadioSelect,choices=(('buy','Buy'),('sell','Sell')))
class Transfer(forms.Form):
    coin_list=tuple((coin.id,coin.title) for coin in List_Coin.objects.all())
    
    to=forms.CharField(max_length=64,validators=[is_user],label=False,required=True ,widget=forms.TextInput(attrs={'class': "form-control w-75",'placeholder':'To'})) 
    coins=forms.ChoiceField(label=False,choices =coin_list,required=True,widget=forms.Select(attrs={"class": "form-control w-75"})) 
    amount=forms.FloatField(label=False,required=True,widget=forms.NumberInput(attrs={"class": "form-control w-75",'placeholder':'Amount'}))
    
# Create your views here.

def index(request):
    url = 'https://api.coincap.io/v2/assets?limit=10'
    
    res = requests.get(url)
    response = json.loads(res.text)
    
    return render(request,'index.html',{'coins':response['data']})

def view_coin(request,id):
    url=f'http://api.coincap.io/v2/assets/{id}'
    res = requests.get(url)
    response = json.loads(res.text)
    return render(request,'view_coin.html',{'coin':response['data']})

def markets(request):
    url = 'https://api.coincap.io/v2/assets'
    
    res = requests.get(url)
    response = json.loads(res.text)
    
    return render(request,'markets.html',{'coins':response['data']})
@login_required
def wallet(request):
    try:

        wallet=Wallet.objects.get(owner=request.user)
        coins=wallet.coins.all()
    except:
        coins="Haven't Deposited anything Yet"

    return render(request,'wallet.html',{'coins':coins})



@login_required
def deposit(request):
    listed_coin=List_Coin.objects.get(coin_id='usd')
    if request.method=="POST":
        form=Deposit(request.POST)
        if form.is_valid():
            amount=form.cleaned_data['amount']           
            
            try:
                wallet=Wallet.objects.get(owner=request.user)
            except:
                wallet=Wallet(
                    owner=request.user
                )
                wallet.save()
            
            try:
                coin=wallet.coins.filter(coin=listed_coin).first()               
                
                if not coin:
                    print('integrity error')
                    raise IntegrityError
                coin.current_coin_amount+=amount
            except IntegrityError:
                coin=Coin(coin=listed_coin)
                coin.save()
                wallet.coins.add(coin)
                coin.current_coin_amount+=amount
            
            
            coin.save()
            wallet.save()
            
            history=History(
                buyer_receiver=User.objects.get(username='cryptohub'),
                seller_sender=request.user,
                transacted_coin=listed_coin,
                transacted_coin_value=1,
                transacted_amount=amount
            )
            history.save()
            return HttpResponseRedirect(reverse("wallet"))
        else:
            return render(request,"deposit.html",{'form':form,"message":"Invalid Amount"})
    
    
    return render(request,'deposit.html',{'form':Deposit()})



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
    
    
def buy_sell(request):
    exchange_per_reserve=1000000
    if request.method=="POST":
        form=Buy_Sell(request.POST)
        
        if form.is_valid():
            amount=form.cleaned_data['amount'] 
            print(form.cleaned_data['coins'])
            coin_id=int(form.cleaned_data['coins']) 
            action=form.cleaned_data['action'] 
            listed_coin=List_Coin.objects.get(pk=coin_id)
            usd_coin=List_Coin.objects.get(coin_id='usd')
            print(listed_coin,listed_coin.coin_id)
            url=f'http://api.coincap.io/v2/assets/{listed_coin.coin_id}'
            res = requests.get(url)
            response = json.loads(res.text)
            current_coin_price=round(float(response['data']['priceUsd']),4)
            exchange_user=User.objects.get(username='cryptohub')
            
            try:
                exchange_wallet=Wallet.objects.get(owner=exchange_user)
            except:
                exchange_wallet=Wallet(owner=exchange_user)
                exchange_wallet.save()
                
            try:
                exchange_coin=exchange_wallet.coins.filter(coin=listed_coin).first() 
                if not exchange_coin:
                    print('integrity error')
                    raise IntegrityError
            except IntegrityError:
                current_amount=exchange_per_reserve/current_coin_price
                exchange_coin=Coin(coin=listed_coin,current_coin_amount=current_amount)
                exchange_coin.save()
                exchange_wallet.coins.add(exchange_coin)
                exchange_wallet.save()
            try:
                user_wallet=Wallet.objects.get(owner=request.user)
            except:
                user_wallet=Wallet(owner=request.user)
                user_wallet.save()
            try:
                user_coin=user_wallet.coins.filter(coin=listed_coin).first()
                if not user_coin:
                    print('integrity error-User side')
                    raise IntegrityError
            except:
                user_coin=Coin(coin=listed_coin)
                user_coin.save()
                user_wallet.coins.add(user_coin)
                user_wallet.save()
                
            
            try:
                user_usd_coin=user_wallet.coins.filter(coin=usd_coin).first()
                if not user_usd_coin:
                    print('integrity error-User Usd side')
                    raise IntegrityError
            except:
                return render(request,'buy_sell.html',{'form':form,'message':'Please Create USD Wallet'})
                
            try:
                exchange_usd_coin=exchange_wallet.coins.filter(coin=usd_coin).first()
                if not exchange_usd_coin:
                    print('integrity error-User Usd side')
                    raise IntegrityError
            except:
                exchange_usd_coin=Coin(coin=usd_coin,current_coin_amount=exchange_per_reserve)
                exchange_usd_coin.save()
                exchange_wallet.coins.add(exchange_usd_coin)
                exchange_wallet.save()
            required_amount=amount*current_coin_price
            if action=='buy':    
                
                if user_usd_coin.current_coin_amount < required_amount:
                    return render(request,'buy_sell.html',{'form':form,'message':'Insufficent (USD) Funds'})
                
                if exchange_coin.current_coin_amount<amount:
                    return render(request,'buy_sell.html',{'form':form,'message':'Insufficent Coins at Exchange'})
                    
                
                user_usd_coin.current_coin_amount-=required_amount
                exchange_usd_coin.current_coin_amount+=required_amount
                exchange_coin.current_coin_amount-=amount
                user_coin.current_coin_amount+=amount
                user_usd_coin.save()
                exchange_usd_coin.save()
                user_coin.save()
                exchange_coin.save()
                user_wallet.save()
                exchange_wallet.save()
                
                history=History(
                buyer_receiver=request.user,
                seller_sender=exchange_user,
                transacted_coin=listed_coin,
                transacted_coin_value=current_coin_price,
                transacted_amount=amount
                                )
                history.save()
                    
                

                return HttpResponseRedirect(reverse("wallet"))
            else:#user selling coins to Exchange
                if exchange_usd_coin.current_coin_amount < required_amount:
                    return render(request,'buy_sell.html',{'form':form,'message':'Insufficent Funds (USD) at Exchange'})
                
                if user_coin.current_coin_amount<amount:
                    return render(request,'buy_sell.html',{'form':form,'message':'Insufficent Coins'})
                
                exchange_usd_coin.current_coin_amount-=required_amount
                user_usd_coin.current_coin_amount+=required_amount
                user_coin.current_coin_amount-=amount
                exchange_coin.current_coin_amount+=amount                
                user_usd_coin.save()
                exchange_usd_coin.save()
                user_coin.save()
                exchange_coin.save()
                user_wallet.save()
                exchange_wallet.save()
                history=History(
                buyer_receiver=exchange_user,
                seller_sender=request.user,
                transacted_coin=listed_coin,
                transacted_coin_value=current_coin_price,
                transacted_amount=amount
                                )
                history.save()
                return HttpResponseRedirect(reverse("wallet"))     
    
    
    
    return render(request,'buy_sell.html',{'form':Buy_Sell()})


def history(request):
    
    history=History.objects.all()
    
    return render(request,'history.html',{'history':history})
    