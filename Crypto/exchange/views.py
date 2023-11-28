from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import User, List_Coin, Coin, Wallet, Watchlist, History, Orders, Order_wallet
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django import forms
import requests
import json
import datetime


def database_listed_coins_updater():
    exchange_per_reserve = 1000000
    try:
        exchange_user = User.objects.get(username='cryptohub')
    except:
        return None
    try:
        exchange_wallet = Wallet.objects.get(owner=exchange_user)
    except:
        exchange_wallet = Wallet(owner=exchange_user)
        exchange_wallet.save()
    if not len(List_Coin.objects.all()):
        coin = List_Coin(
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
            coins = List_Coin(
                coin_id=item['id'],
                symbol=item['symbol'],
                title=item['name'],
                logo_url=f"https://cryptologos.cc/logos/{item['id']}-{item['symbol'].lower()}-logo.png")
            coins.save()
        print('Coins Updated Successfully')
        print('Coin Purchase Started')
        listed_coin = List_Coin.objects.get(coin_id='usd')
        current_amount = exchange_per_reserve/1
        exchange_coin = Coin(coin=listed_coin, current_coin_amount=current_amount,
                             last_purchased=datetime.datetime.now())
        exchange_coin.save()
        exchange_wallet.coins.add(exchange_coin)
        exchange_wallet.save()
        print(f"Purchased {current_amount} {'usd'} at {1}/USD ")

        for coin in response['data']:

            current_coin_price = float(coin['priceUsd'])

            listed_coin = List_Coin.objects.get(coin_id=coin['id'])

            current_amount = exchange_per_reserve/current_coin_price
            current_amount = current_amount

            exchange_coin = Coin(
                coin=listed_coin, current_coin_amount=current_amount, last_purchased=datetime.datetime.now())
            exchange_coin.save()

            exchange_wallet.coins.add(exchange_coin)
            exchange_wallet.save()
            print(
                f"Purchased {current_amount} {coin['id']} at {current_coin_price}/USD ")


database_listed_coins_updater()


def is_user(username):
    if not username in [user.username for user in User.objects.all()]:
        raise ValidationError('Invalid User')


def get_coin_list():
    coin_list = tuple((coin.id, coin.title)
                      for coin in List_Coin.objects.all())
    return coin_list[2:]


def get_user_list():
    user_list = tuple((user.username, user.username)
                      for user in User.objects.all().exclude(username='cryptohub'))
    return user_list


class Deposit(forms.Form):
    amount = forms.IntegerField(label=False, required=True, widget=forms.NumberInput(
        attrs={"class": "form-control w-75 mb-2 ms-3", 'placeholder': 'Deposit USD'}))


class Buy_Sell(forms.Form):

    coins = forms.ChoiceField(label=False, choices=get_coin_list(
    ), required=True, widget=forms.Select(attrs={"class": "form-control w-75 mb-2 ms-3"}))
    amount = forms.FloatField(label=False, required=True, widget=forms.NumberInput(
        attrs={"class": "form-control w-75 mb-2 ms-3", 'placeholder': 'Amount'}))
    action = forms.ChoiceField(label=False, widget=forms.RadioSelect(
        attrs={"class": "form-check-inline mb-2 ms-2","id":"buy_sell_radio_btn"}), choices=(('buy', 'Buy'), ('sell', 'Sell')))


class Transfer(forms.Form):
    # For live updation of users in forms when database changes
    def __init__(self, *args, **kwargs):
        super(Transfer, self).__init__(*args, **kwargs)
        self.fields['to'] = forms.ChoiceField(choices=get_user_list(
        ), required=True, widget=forms.Select(attrs={"class": "form-control w-75 mb-2 ms-3"}))
        self.fields['coins'] = forms.ChoiceField(label=False, choices=get_coin_list(
        ), required=True, widget=forms.Select(attrs={"class": "form-control w-75 mb-2 ms-3"}))
        self.fields['amount'] = forms.FloatField(label=False, required=True, widget=forms.NumberInput(
            attrs={"class": "form-control w-75 mb-2 ms-3", 'placeholder': 'Amount'}))


class Create_orders(forms.Form):
    coins = forms.ChoiceField(label=False, choices=get_coin_list(
    ), required=True, widget=forms.Select(attrs={"class": "form-control w-75 mb-2 ms-3"}))
    amount = forms.FloatField(label=False, required=True, widget=forms.NumberInput(
        attrs={"class": "form-control w-75 mb-2 ms-3", 'placeholder': 'No of Coins'}))
    price_per_coin = forms.FloatField(label=False, required=True, widget=forms.NumberInput(
        attrs={"class": "form-control w-75 mb-2 ms-3", 'placeholder': 'Required Price/Coin'}))
    action = forms.ChoiceField(label=False, widget=forms.RadioSelect( attrs={"class": "form-check-inline mb-2 ms-2","id":"order_radio_btn"}), choices=(
        ('buy', 'Buy Order'), ('sell', 'Sell Order')))


# Create your views here.

def index(request):
    url = 'https://api.coincap.io/v2/assets?limit=10'

    res = requests.get(url)
    response = json.loads(res.text)

    return render(request, 'index.html', {'coins': response['data']})


def view_coin(request, id):
    
    coin=List_Coin.objects.get(coin_id=id)
    
    try:
        watchlists=Watchlist.objects.get(watcher=request.user)
        watchlisted= coin in watchlists.watch_list.all()
        print(watchlisted)
    except:
        watchlisted=False
   
    return render(request, 'view_coin.html', {'coin': coin.serialize(),'watchlisted':watchlisted})


def coin_data(request, id):
    if not id == "usd":
        url = f'http://api.coincap.io/v2/assets/{id}'
        res = requests.get(url)
        response = json.loads(res.text)
        coin = response['data']
    else:
        coin ={'priceUsd': 1, 'symbol': 'USD', 'name': 'US Dollar','id':'usd'}

    return JsonResponse({'coin':coin},safe=False)



def markets(request):
    
    coins = List_Coin.objects.all()
    paginator = Paginator(coins, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    try:
        watch = Watchlist.objects.get(watcher=request.user)
        lists=watch.watch_list.all()
        watchlists=[coin.coin_id for coin in lists]  
    except:
        watchlists=[]

    return render(request, 'markets.html', {'coins': page_obj,'watchlists':watchlists})

@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":        
        email = request.POST["email"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        profile_url=request.POST["profile_url"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password and confirmation:
            
            if password != confirmation:
                return render(request, "register.html", {
                    "message": "Passwords must match.",'user':user
                })

        # Attempt to create new user
        try:
            if email and (not email == user.email):
                user.email=email
            if firstname and (not firstname == user.first_name):
                user.first_name=firstname
            if lastname and (not lastname==user.last_name):
                user.last_name=lastname
            if profile_url and (not profile_url==user.profile_url):
                user.profile_url=profile_url
            if password:
                password=make_password(password,hasher='default')
                user.password=password
            user.save()
        except IntegrityError:
            return render(request, "profile.html", {'user':user           
            })
        
        return render(request, 'profile.html',{'user':user,'message':'Saved Succesfully'})
    else:     
    
         return render(request, 'profile.html',{'user':user})


@login_required
def wallet(request):
    try:

        wallet = Wallet.objects.get(owner=request.user)
        coins = wallet.coins.all()
        paginator = Paginator(coins, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except:
        coins = []

    return render(request, 'wallet.html', {'coins': page_obj})


@login_required
def deposit(request):
    listed_coin = List_Coin.objects.get(coin_id='usd')
    if request.method == "POST":
        form = Deposit(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            try:
                wallet = Wallet.objects.get(owner=request.user)
            except:
                wallet = Wallet(
                    owner=request.user
                )
                wallet.save()

            try:
                coin = wallet.coins.filter(coin=listed_coin).first()

                if not coin:
                    print('integrity error')
                    raise IntegrityError
                coin.current_coin_amount += amount
            except IntegrityError:
                coin = Coin(coin=listed_coin,
                            last_purchased=datetime.datetime.now())
                coin.save()
                wallet.coins.add(coin)
                coin.current_coin_amount += amount

            coin.save()
            wallet.save()

            history = History(
                to_user=User.objects.get(username='cryptohub'),
                from_user=request.user,
                transacted_coin=listed_coin,
                transacted_coin_value=1,
                transacted_amount=amount,
                transact_action='Deposited'
            )
            history.save()
            return HttpResponseRedirect(reverse("wallet"))
        else:
            return render(request, "deposit.html", {'form': form, "message": "Invalid Amount"})

    return render(request, 'deposit.html', {'form': Deposit()})


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
    if not request. user. is_anonymous:

        exchange_per_reserve = 1000000
        if request.method == "POST":
            form = Buy_Sell(request.POST)

            if form.is_valid():
                amount = form.cleaned_data['amount']
                print(form.cleaned_data['coins'])
                coin_id = int(form.cleaned_data['coins'])
                action = form.cleaned_data['action']
                coin=List_Coin.objects.get(pk=coin_id)
                url = f'http://api.coincap.io/v2/assets/{coin.coin_id}'
                res = requests.get(url)
                response = json.loads(res.text)
                current_coin_price = round(float(response['data']['priceUsd']), 4)

                exchange_user = User.objects.get(username='cryptohub')

                listed_coin = List_Coin.objects.get(pk=coin_id)
                usd_coin = List_Coin.objects.get(coin_id='usd')

                try:
                    exchange_wallet = Wallet.objects.get(owner=exchange_user)
                except:
                    exchange_wallet = Wallet(owner=exchange_user)
                    exchange_wallet.save()

                try:
                    exchange_coin = exchange_wallet.coins.filter(
                        coin=listed_coin).first()
                    if not exchange_coin:
                        print('integrity error')
                        raise IntegrityError
                except IntegrityError:
                    current_amount = exchange_per_reserve/current_coin_price
                    exchange_coin = Coin(
                        coin=listed_coin, current_coin_amount=current_amount)
                    exchange_coin.save()
                    exchange_wallet.coins.add(exchange_coin)
                    exchange_wallet.save()
                try:
                    user_wallet = Wallet.objects.get(owner=request.user)
                except:
                    user_wallet = Wallet(owner=request.user)
                    user_wallet.save()
                try:
                    user_coin = user_wallet.coins.filter(coin=listed_coin).first()
                    if not user_coin:
                        print('integrity error-User side')
                        raise IntegrityError
                except:
                    user_coin = Coin(coin=listed_coin)
                    user_coin.save()
                    user_wallet.coins.add(user_coin)
                    user_wallet.save()

                try:
                    user_usd_coin = user_wallet.coins.filter(coin=usd_coin).first()
                    if not user_usd_coin:
                        print('integrity error-User Usd side')
                        raise IntegrityError
                except:
                    user_usd_coin = Coin(
                        coin=usd_coin)
                    user_usd_coin.save()
                    user_wallet.coins.add(exchange_usd_coin)
                    user_wallet.save()
                    

                try:
                    exchange_usd_coin = exchange_wallet.coins.filter(
                        coin=usd_coin).first()
                    if not exchange_usd_coin:
                        print('integrity error-exchange Usd side')
                        raise IntegrityError
                except:
                    exchange_usd_coin = Coin(
                        coin=usd_coin, current_coin_amount=exchange_per_reserve)
                    exchange_usd_coin.save()
                    exchange_wallet.coins.add(exchange_usd_coin)
                    exchange_wallet.save()
                required_amount = amount*current_coin_price
                if action == 'buy':

                    if user_usd_coin.current_coin_amount < required_amount:
                        return render(request, 'buy_sell.html', {'form': form, 'message': 'Insufficent (USD) Funds'})

                    if exchange_coin.current_coin_amount < amount:
                        return render(request, 'buy_sell.html', {'form': form, 'message': 'Insufficent Coins at Exchange'})

                    user_usd_coin.current_coin_amount -= required_amount
                    exchange_usd_coin.current_coin_amount += required_amount
                    exchange_coin.current_coin_amount -= amount
                    user_coin.current_coin_amount += amount
                    user_usd_coin.save()
                    exchange_usd_coin.save()
                    user_coin.save()
                    exchange_coin.save()
                    user_wallet.save()
                    exchange_wallet.save()

                    history = History(
                        to_user=request.user,
                        from_user=exchange_user,
                        transacted_coin=listed_coin,
                        transacted_coin_value=current_coin_price,
                        transacted_amount=amount,
                        transact_action='Sold'
                    )
                    history.save()

                    return HttpResponseRedirect(reverse("wallet"))
                else:  # user selling coins to Exchange
                    if exchange_usd_coin.current_coin_amount < required_amount:
                        return render(request, 'buy_sell.html', {'form': form, 'message': 'Insufficent Funds (USD) at Exchange'})

                    if user_coin.current_coin_amount < amount:
                        return render(request, 'buy_sell.html', {'form': form, 'message': 'Insufficent Coins'})

                    exchange_usd_coin.current_coin_amount -= required_amount
                    user_usd_coin.current_coin_amount += required_amount
                    user_coin.current_coin_amount -= amount
                    exchange_coin.current_coin_amount += amount
                    user_usd_coin.save()
                    exchange_usd_coin.save()
                    user_coin.save()
                    exchange_coin.save()
                    user_wallet.save()
                    exchange_wallet.save()

                    history = History(
                        to_user=exchange_user,
                        from_user=request.user,
                        transacted_coin=listed_coin,
                        transacted_coin_value=current_coin_price,
                        transacted_amount=amount,
                        transact_action='Sold'
                    )
                    history.save()
                    return HttpResponseRedirect(reverse("wallet"))
    

    return render(request, 'buy_sell.html', {'form': Buy_Sell()})

@login_required
def history(request):

    history = History.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
    history = history.order_by("-transaction_on").all()
    paginator = Paginator(history, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'history.html', {'history': page_obj})

@login_required
def transfer(request):
    if request.method == "POST":
        form = Transfer(request.POST)
        if form.is_valid():
            amount = float(form.cleaned_data['amount'])

            id = int(form.cleaned_data['coins'])
            to = form.cleaned_data['to']
            transfer_coin = List_Coin.objects.get(pk=id)
            url = f'http://api.coincap.io/v2/assets/{transfer_coin.coin_id}'
            res = requests.get(url)
            response = json.loads(res.text)
            current_coin_price = round(float(response['data']['priceUsd']), 4)
            if to == request.user.username:
                return render(request, 'transfer.html', {'form': form, 'message': 'You can not send money to yourself'})
            receiver = User.objects.get(username=to)
            try:
                sender_wallet = Wallet.objects.get(owner=request.user)
            except:
                return render(request, 'transfer.html', {'form': form, 'message': 'Please add funds and create a wallet first'})
            try:
                sender_coin = sender_wallet.coins.filter(
                    coin=transfer_coin).first()
                if not sender_coin:
                    raise IntegrityError
            except:
                return render(request, 'transfer.html', {'form': form, 'message': f'You do not have a {transfer_coin.title} wallet'})

            if sender_coin.current_coin_amount < amount:
                return render(request, 'transfer.html', {'form': form, 'message': 'Insufficient Funds'})

            try:
                receiver_wallet = Wallet.objects.get(owner=receiver)
            except:
                receiver_wallet = Wallet(owner=receiver)
                receiver_wallet.save()
            try:
                receiver_coin = receiver_wallet.coins.filter(
                    coin=transfer_coin).first()
                if not receiver_coin:
                    raise IntegrityError
            except:
                receiver_coin = Coin(coin=transfer_coin)
                receiver_coin.save()
                receiver_wallet.coins.add(receiver_coin)
                receiver_wallet.save()

            sender_coin.current_coin_amount -= amount
            receiver_coin.current_coin_amount += amount
            sender_coin.save()
            receiver_coin.save()
            sender_wallet.save()
            receiver_wallet.save()
            history = History(
                to_user=receiver,
                from_user=request.user,
                transacted_coin=transfer_coin,
                transacted_coin_value=current_coin_price,
                transacted_amount=amount,
                transact_action='Transferred'
            )
            history.save()
            return HttpResponseRedirect(reverse("wallet"))

        else:
            return render(request, 'transfer.html', {'form': form})

    return render(request, 'transfer.html', {'form': Transfer()})



@login_required
def add_watchlist(request, id):
    # id=coin_id not pk
    coin = List_Coin.objects.get(coin_id=id)

    try:
        watch = Watchlist.objects.get(watcher=request.user)
        watch.watch_list.add(coin)
    except:
        watch = Watchlist(watcher=request.user)
        watch.save()
        watch.watch_list.add(coin)

    watch.save()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def remove_watchlist(request, id):
    # id=coin_id not pk
    coin = List_Coin.objects.get(coin_id=id)

    try:
        watch = Watchlist.objects.get(watcher=request.user)
        watch.watch_list.remove(coin)
    except:
        pass

    watch.save()
    return HttpResponseRedirect(reverse("watchlist"))


def watchlist(request):
    try:
        watch = Watchlist.objects.get(watcher=request.user)
        
        watchlists=watch.watch_list.all()
        paginator = Paginator(watchlists, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except:
        watchlists=[]
    
    return render(request, 'watchlist.html', {'watchlists': page_obj})


def my_orders(request):
    orders = Orders.objects.filter(lister=request.user)
    orders = orders.order_by("-created").all()
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'my_orders.html', {'orders': page_obj})


def all_orders(request):
    orders = Orders.objects.all().filter(is_fulfilled=False, is_closed=False)
    orders = orders.order_by("-created").all()
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'all_orders.html', {'orders': page_obj})


def create_orders(request):
    if request.method == "POST":
        form = Create_orders(request.POST)
        if form.is_valid():
            id = int(form.cleaned_data['coins'])
            amount = float(form.cleaned_data['amount'])
            price_per_coin = float(form.cleaned_data['price_per_coin'])
            action = form.cleaned_data['action']
            print(id, amount, price_per_coin, action)
            order_coin = List_Coin.objects.get(pk=id)
            if action == 'buy':
                usd_coin = List_Coin.objects.get(coin_id='usd')
            try:
                lister_wallet = Wallet.objects.get(owner=request.user)
            except:
                return render(request, 'create_orders.html', {'form': form, 'message': 'Please add funds and create a wallet first'})
            try:
                if action == 'buy':
                    lister_coin = lister_wallet.coins.filter(
                        coin=usd_coin).first()
                    if not lister_coin:
                        raise IntegrityError
                else:  # sell
                    lister_coin = lister_wallet.coins.filter(
                        coin=order_coin).first()
                    if not lister_coin:
                        raise IntegrityError
            except:
                return render(request, 'create_orders.html', {'form': form, 'message': f"You do not have a {usd_coin.title if action=='buy' else order_coin.title} wallet"})

            Total_amount = amount
            if action == 'buy':
                Total_amount = amount*price_per_coin
            if lister_coin.current_coin_amount < Total_amount:
                return render(request, 'create_orders.html', {'form': form, 'message': 'Insufficient Funds to place an Order'})

            order = Orders(
                lister=request.user,
                order_coin=order_coin,
                order_coin_no=amount,
                order_price_per_coin=price_per_coin,
                order_amount=price_per_coin*amount,
                is_buy=action == 'buy',
                created=datetime.datetime.now()
            )
            order.save()
            temp_wallet = Order_wallet(
                lister=request.user,
                order=order,
                temp_coin=usd_coin if action == 'buy' else order_coin,
                frozen_amount=Total_amount

            )
            temp_wallet.save()
            if temp_wallet.id and order.id:
                lister_coin.current_coin_amount -= Total_amount
                lister_coin.save()
                lister_wallet.save()

            return HttpResponseRedirect(reverse("my_orders"))

        else:
            return render(request, 'create_orders.html', {'form': form, 'message': 'Invalid Details'})

    return render(request, 'create_orders.html', {'form': Create_orders()})


def order_deal(request, action):
    if request.method != "POST":
        return JsonResponse({'status':'false',"message": "POST request required."}, status=400)
    data = json.loads(request.body)
    order_id = int(data.get('id', ""))
    owner = data.get('owner', "")

    lister = User.objects.get(username=owner)
    
    order = Orders.objects.get(pk=order_id)
    doer = request.user
    print('Lister:',lister)
    print('doer:',doer)

    order_coin = order.order_coin
    print(order_coin)
    order_price_per_coin = order.order_price_per_coin
    order_amount = order.order_amount
    order_coin_no = order.order_coin_no
    print(order_coin_no)

    lister_wallet = Wallet.objects.get(owner=lister)
    lister_temp_wallet = Order_wallet.objects.get(order=order)
    try:
        lister_coin = lister_wallet.coins.filter(coin=order_coin).first()
        if not lister_coin:
            raise IntegrityError
    except:
        lister_coin = Coin(coin=order_coin)
        lister_coin.save()
        lister_wallet.coins.add(lister_coin)
        lister_wallet.save()

    usd_coin = List_Coin.objects.get(coin_id='usd')
    if not lister == doer:
        try:
            doer_wallet = Wallet.objects.get(owner=doer)
        except:
            return JsonResponse({'status':'false',"message": "Wallet required."}, status=400)
        try:
            doer_coin = doer_wallet.coins.filter(coin=order_coin).first()
            if not doer_coin:
                raise IntegrityError
        except:
            doer_coin = Coin(coin=order_coin)
            doer_coin.save()
            doer_wallet.coins.add(doer_coin)
            doer_wallet.save()
        try:
            doer_usd_coin = doer_wallet.coins.filter(coin=usd_coin).first()
            if not doer_usd_coin:
                raise IntegrityError
        except:
            doer_usd_coin = Coin(coin=usd_coin)
            doer_usd_coin.save()
            doer_wallet.coins.add(doer_coin)
            doer_wallet.save()

        try:
            lister_usd_coin = lister_wallet.coins.filter(coin=usd_coin).first()
            if not lister_usd_coin:
                raise IntegrityError
        except:
            lister_usd_coin = Coin(coin=usd_coin)
            lister_usd_coin.save()
            lister_wallet.coins.add(lister_usd_coin)
            lister_wallet.save()
    else:
        try:
            lister_usd_coin = lister_wallet.coins.filter(coin=usd_coin).first()
            if not lister_usd_coin:
                raise IntegrityError
        except:
            lister_usd_coin = Coin(coin=usd_coin)
            lister_usd_coin.save()
            lister_wallet.coins.add(lister_usd_coin)
            lister_wallet.save()
    
    if action == 'buy':
        
        try:
            doer_usd_coin = doer_wallet.coins.filter(coin=usd_coin).first()
            if not doer_usd_coin:
                raise IntegrityError
        except:
            return JsonResponse({'status':'false',"message": "USD wallet required."}, status=400)

        if doer_usd_coin.current_coin_amount < order_amount:
            return JsonResponse({'status':'false',"error": "Insufficient Funds."}, status=400)

        doer_coin.current_coin_amount += lister_temp_wallet.frozen_amount
        doer_coin.save()
        
        lister_usd_coin.current_coin_amount += order_amount
        doer_usd_coin.current_coin_amount -= order_amount
        lister_usd_coin.save()
        doer_usd_coin.save()
        lister_wallet.save()
        doer_wallet.save()
        order.is_fulfilled = True
        order.fulfilled_on = datetime.datetime.now()
        order.save()
        history = History(
            to_user=doer,
            from_user=lister,
            transacted_coin=order_coin,
            transacted_coin_value=order_price_per_coin,
            transacted_amount=order_coin_no,
            transact_action='Sold'
        )
        history.save()
        lister_temp_wallet.delete()
        if history.id:
            return JsonResponse({'status':'true',"message": "Buy action Completed successfully."}, status=201)
        else:
            return JsonResponse({'status':'false',"message": "Something went wrong."}, status=400)
        
        
    if action == 'sell':
        try:            
            if not doer_coin:
                raise IntegrityError
        except:
            return JsonResponse({'status':'false',"message": f"{order_coin.title} wallet required."}, status=400)

        if doer_coin.current_coin_amount < order_coin_no:
            return JsonResponse({'status':'false',"error": "Insufficient Funds."}, status=400)

        doer_usd_coin.current_coin_amount += lister_temp_wallet.frozen_amount#now temp wallet contains usd
        doer_usd_coin.save()
        
        lister_coin.current_coin_amount += order_coin_no
        doer_coin.current_coin_amount -= order_coin_no
        lister_coin.save()
        doer_coin.save()
        lister_wallet.save()
        doer_wallet.save()
        order.is_fulfilled = True
        order.fulfilled_on = datetime.datetime.now()
        order.save()
        history = History(
            to_user=lister,
            from_user=doer,
            transacted_coin=order_coin,
            transacted_coin_value=order_price_per_coin,
            transacted_amount=order_coin_no,
            transact_action='Sold'
        )
        history.save()
        lister_temp_wallet.delete()
        if history.id:
            return JsonResponse({'status':'true',"message": "Sell action Completed successfully."}, status=201)
        else:
            return JsonResponse({'status':'false',"message": "Something went wrong."}, status=400)
    if action == 'close':
        if lister==doer:
            print(lister_temp_wallet.temp_coin.coin_id)
            if lister_temp_wallet.temp_coin.coin_id=='usd':
                lister_usd_coin.current_coin_amount+=lister_temp_wallet.frozen_amount
                lister_usd_coin.save()
                lister_wallet.save()
                lister_temp_wallet.delete()
            else:
                lister_coin.current_coin_amount+=lister_temp_wallet.frozen_amount
                lister_coin.save()
                lister_wallet.save()
                lister_temp_wallet.delete()
                
            order.is_closed=True
            order.closed_on=datetime.datetime.now()
            order.save()

    return JsonResponse({'status':'true',"message": "Action Completed successfully."}, status=201)


def info(request,details):
    if details=='wallet':
        if not request. user. is_anonymous:
            try:
                wallet=Wallet.objects.get(owner=request.user)
                return JsonResponse({"wallet":wallet.serialize()},safe=False)
            except:
                return JsonResponse({'status':'false',"message": "Wallet does not exist!"},status=404)
        else:
            return JsonResponse({'status':'false',"message": "Please log in!"},status=404)
    elif details=='list_coin':
        try:            
            coins=List_Coin.objects.all().exclude(coin_id='usd')
            all_coins=List_Coin.objects.all()
            return JsonResponse({"coins":[coin.coin_id for coin in coins],
                                 "all_coins":{coin.id:coin.coin_id for coin in all_coins}},safe=False)
        except:
            return JsonResponse({'status':'false',"message": "List does not exist!"},status=404)
        
    elif details=='watchlist':
        if not request. user. is_anonymous:

            try:
                watch=Watchlist.objects.get(watcher=request.user)
                watchlist=[coin.coin_id for coin in watch.watch_list.all()]
                return JsonResponse({"watchlist":watchlist},safe=False)
            
            except:
                return JsonResponse({'status':'false',"message": "List does not exist!"},status=404)
        else:
            return JsonResponse({'status':'false',"message": "Please log in!"},status=404)

            
def price_history(request,**values):
    import datetime
    id=values['id']
    period=values['period']
    print(id,period)
    list_coin=List_Coin.objects.get(coin_id=id)
    
    url = f'https://api.coincap.io/v2/assets/{id}/history?interval={period}'
    res = requests.get(url)
    response = json.loads(res.text)
    coin = response['data']
    priceUsd=[]
    time=[]
    for item in coin:
        priceUsd.append(float(item['priceUsd']))
        time.append(item['date'].replace('T',' ').replace('.000Z',''))

    
    return JsonResponse({'priceUsd':priceUsd,'time':time,'name':list_coin.title,'period':period},safe=False)     



def test(request):

    


    
    

    
    return render(request, 'test.html')
