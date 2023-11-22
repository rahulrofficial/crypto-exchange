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

class Deposit(forms.Form):
    amount=forms.IntegerField(label=False,required=True,widget=forms.NumberInput(attrs={"class": "form-control w-75",'placeholder':'Deposit'}))

class Buy_Sell(forms.Form):
    coin_list=[]
    coins=forms.MultipleChoiceField(choices =coin_list,required=True,widget=forms.SelectMultiple(attrs={"class": "form-control w-75"})) 
    amount=forms.FloatField(label=False,required=True,widget=forms.NumberInput(attrs={"class": "form-control w-75",'placeholder':'Amount'}))

class Transfer(forms.Form):
    coin_list=[]
    user_list=[]
    coins=forms.MultipleChoiceField(choices =coin_list,required=True,widget=forms.SelectMultiple(attrs={"class": "form-control w-75"})) 
    amount=forms.FloatField(label=False,required=True,widget=forms.NumberInput(attrs={"class": "form-control w-75",'placeholder':'Amount'}))
    to=forms.MultipleChoiceField(choices =user_list,required=True,widget=forms.SelectMultiple(attrs={"class": "form-control w-75"})) 
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
            
            print(listed_coin.symbol)
            try:
                wallet=Wallet.objects.get(owner=request.user)
            except:
                wallet=Wallet(
                    owner=request.user
                )
                wallet.save()
            
            try:
                coin=wallet.coins.filter(coin=listed_coin).first()
                coin.current_coin_amount+=amount
                print(coin)
                if not coin:
                    print('integrity erro')
                    raise IntegrityError
            except IntegrityError:
                coin=Coin(coin=listed_coin)
                coin.save()
                wallet.coins.add(coin)
                coin.current_coin_amount+=amount
            
            
            coin.save()
            wallet.save()
            
            history=History(
                buyer_receier=User.objects.get(username='cryptohub'),
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