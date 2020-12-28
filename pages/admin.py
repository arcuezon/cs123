from django.contrib import admin
from .models import Item, Profile, Cart, Address, AddressInfo

# Register your models here.
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(AddressInfo)