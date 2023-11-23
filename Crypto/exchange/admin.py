from django.contrib import admin
from .models import User,List_Coin,Coin,Wallet,Watchlist,History,Orders,Order_wallet
# Register your models here.
admin.site.register(User)
admin.site.register(List_Coin)
admin.site.register(Coin)
admin.site.register(Wallet)
admin.site.register(Watchlist)
admin.site.register(History)
admin.site.register(Orders)
admin.site.register(Order_wallet)