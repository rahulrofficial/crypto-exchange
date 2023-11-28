from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("view_coin/<str:id>", views.view_coin, name="view_coin"),
    path("markets", views.markets, name="markets"),
    path("deposit", views.deposit, name="deposit"),
    path("wallet", views.wallet, name="wallet"),
    path("buy_sell", views.buy_sell, name="buy_sell"),
    path("history", views.history, name="history"),
    path("transfer", views.transfer, name="transfer"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<str:id>", views.add_watchlist, name="add_watchlist"),
    path("remove watchlist/<str:id>", views.remove_watchlist, name="remove_watchlist"),
    path("create_orders", views.create_orders, name="create_orders"),
    path("my_orders", views.my_orders, name="my_orders"),
    path("all_orders", views.all_orders, name="all_orders"),
    path("test", views.test, name="test"),


    #apis
    path("order_deal/<str:action>", views.order_deal, name="order_deal"),
    path("info/<str:details>", views.info, name="info"),
    path("coin_data/<str:id>", views.coin_data, name="coin_data")
]