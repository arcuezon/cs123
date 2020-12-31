from django.contrib import admin
from .models import Item, Profile, Cart, OrderQuantity

# Register your models here.
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(OrderQuantity)