from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view_coin/<str:id>", views.view_coin, name="view_coin"),
    path("markets", views.markets, name="markets"),
    path("deposit", views.deposit, name="deposit"),
    path("wallet", views.wallet, name="wallet"),
    path("buy_sell", views.buy_sell, name="buy_sell"),
    path("history", views.history, name="history")
]