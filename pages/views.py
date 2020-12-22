from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate

from .models import Item

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def profile_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, "profile.html",{})
    
    return render(request, 'registration/login.html', {})

    

def about_view(request):
    return render(request, "about-us.html", {})

def index(request, *args, **kwargs):
    all_items = Item.objects.all()
    context = {
        'all_items': all_items,
        'title': 'Shop'
    }
    return render(request, "home.html", context)