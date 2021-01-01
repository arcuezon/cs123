"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import *

urlpatterns = [
    path('admin/', admin.site.urls), #default admin site
    path('', index, name='home'), #splash page/index, main shop page
    path('accounts/',  include('django.contrib.auth.urls')), #for login
    path('profile/', profile_view, name='profile'), #account information
    path('about-us/', about_view, name='about us'), #about us page for the website
    path('signup/', signup, name='signup'), #user signup page
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:item_id>/', add_cart, name='add to cart'),
    path('item/<int:item_id>/', item_view),
    path('remove-item/<int:item_id>/', remove_item),
    path('checkout/', checkout_view), 
]   
