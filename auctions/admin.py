from django.contrib import admin
from .models import User, Listing,WatchList, Command, Auction

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)

admin.site.register(WatchList)
admin.site.register(Command)
admin.site.register(Auction)