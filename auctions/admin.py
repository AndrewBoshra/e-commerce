from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Watchlist)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)