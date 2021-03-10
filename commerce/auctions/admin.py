from django.contrib import admin

from .models import Auctionlist,Category,Watchlist,Comments,Bids

# Register your models here.
admin.site.register(Auctionlist)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bids)