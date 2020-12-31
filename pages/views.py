from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.forms import SignUpForm
import operator
from .models import Cart, Profile, Item

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #Adding the address inputs
            user.profile.address_line_1 = form.cleaned_data.get('address_line_1')
            user.profile.address_line_2 = form.cleaned_data.get('address_line_2')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.zip_code = form.cleaned_data.get('zip_code')
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/accounts/login/')
def add_cart(request):
    if request.method == 'GET' and 'item' in request.GET:
        print('Request made.')
        item_id = request.GET['item']
        cart, _ = Cart.objects.get_or_create(customer=request.user.profile)
        cart.add_item(item_id)

    else:
        #Todo: If item-id doesn't exist
        pass

    return cart_view(request)

@login_required(login_url='/accounts/login/')
def cart_view(request):
    if Cart.objects.filter(customer=request.user.profile).exists():
        cart = Cart.objects.get(customer=request.user.profile)
        cart_items = cart.ordered_items.all()

        quantity = []
        for cart_item in cart_items:
            quantity.append(cart.item_quantity.get(product = cart_item).quantity)
        
        cart_quantity = zip(cart_items, quantity)

        context = {
            'cart': cart_quantity,
            'title': 'Shop'
        }
    
    else:
          context = {
            'title': 'Shop: My Cart'
        }
    

    return render(request, "cart.html", context)
