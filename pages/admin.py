from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(CartDetails)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Review)