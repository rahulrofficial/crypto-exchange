from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import User
import requests
import json 


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