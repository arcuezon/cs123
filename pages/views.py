from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import operator

from .models import Item, Profile

#Home page (replaced by index)
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

#Profile page
#Require users to login to view this page. Redirect if not.
@login_required(login_url='/accounts/login/')
def profile_view(request, *args, **kwargs):

    return render(request, "profile.html",{})

#About page
def about_view(request):
    return render(request, "about-us.html", {})

#Home and Shop page that passes all Items to the Frontend
def index(request, *args, **kwargs):

    if request.method == 'GET' and 'filter' in request.GET:
        print('Request made.')
        filter_req = request.GET['filter']
        all_items = Item.objects.order_by(filter_req)
    else:
        all_items = Item.objects.order_by("name")

    context = {
        'all_items': all_items,
        'title': 'Shop'
    }

    return render(request, "home.html", context)

#Sign-up page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})