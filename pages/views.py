from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.forms import SignUpForm
import operator
from .models import CartDetails, Profile, Item, Address, Review, Order, OrderDetails

# Profile page
# Require users to login to view this page. Redirect if not.


@login_required(login_url='/accounts/login/')
def profile_view(request, *args, **kwargs):
    address = Address.objects.get(user = request.user.profile)
    context = {
        "address": address,
        "title": "Shop: My Profile"
    }
    return render(request, "profile.html", context)

# About page


def about_view(request):
    return render(request, "about-us.html", {})

# Home and Shop page that passes all Items to the Frontend


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

# Sign-up page


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # Adding the address inputs
            address = Address.objects.create(
                user = user.profile,
                address_line_1=form.cleaned_data.get('address_line_1'),
                address_line_2=form.cleaned_data.get('address_line_2'),
                city=form.cleaned_data.get('city'),
                country=form.cleaned_data.get('country'),
                zip_code=form.cleaned_data.get('zip_code'),
            )
            user.profile.birth_date = form.cleaned_data.get("birth_date")
            address.save()
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def add_cart(request, item_id):

    item = Item.objects.get(item_id=item_id)
    cart, cart_created = CartDetails.objects.get_or_create(
        item=item, user=request.user)

    if not cart_created:
        cart.quantity += 1
        cart.save()


    return redirect('/my-cart')


@login_required(login_url='/accounts/login/')
def cart_view(request):
    if CartDetails.objects.filter(user=request.user).exists():
        cart = CartDetails.objects.filter(user=request.user)

        cart_items = []
        quantity = []
        subtotal = []
        for cart_item in cart:
            cart_items.append(cart_item.item)
            quantity.append(cart_item.quantity)
            subtotal.append(cart_item.item.price * cart_item.quantity)

        cart_quantity = zip(cart_items, quantity, subtotal)

        context = {
            'cart': cart_quantity,
            'total': sum(subtotal),
            'title': 'Shop: My Cart'
        }

    else:
        context = {
            'title': 'Shop: My Cart'
        }

    return render(request, "cart.html", context)

def item_view(request, item_id):
    item = Item.objects.get(item_id = item_id)

    if Review.objects.filter(item = item).exists():
        reviews = Review.objects.filter(item = item)

        context ={
            "item": item,
            "reviews": reviews,
            "title": item.name
        }
    
    else:
        context ={
            "item": item,
            "title": item.name
        }

    return render(request, "item.html", context)

def remove_item(request, item_id):
    item = Item.objects.get(item_id = item_id)

    cart = CartDetails.objects.get(user=request.user, item=item)

    if cart.quantity == 1:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()

    return redirect('/my-cart')

#Fix duplication because request every checkout. Better to confirm here.
def checkout_view(request):
    order = Order.objects.create(user = request.user.profile)
    cart = CartDetails.objects.filter(user = request.user)

    order_details = []
    subtotals = []
    for item_cart in cart:
        order_item = OrderDetails.objects.create(
            order_id = order,
            item = item_cart.item,
            quantity = item_cart.quantity,
        )
        subtotals.append(item_cart.item.price * item_cart.quantity)
        order_details.append(order_item)

    order_subtotal = zip(order_details, subtotals)

    cart.delete()

    context = {
        "order_num": order.order_id,
        "order": order_subtotal,
        "total": sum(subtotals),
        "title": f"Order no: {order.order_id}",
    }

    return render(request, "checkout.html", context)

def orders_view(request):
    all_orders = Order.objects.filter(user = request.user.profile).order_by('created_date')

    order_ids = []
    order_status = []
    order_collect = []
    totals = []
    for orders in all_orders:
        order_ids.append(orders.order_id)
        order_status.append(orders.get_status)
        order = OrderDetails.objects.filter(order_id = orders.order_id)

        single_order = []
        total_order = 0
        for item in order:
            single_order.append(item)
            total_order += int(item.get_subtotal())
        
        order_collect.append(single_order)
        totals.append(total_order)



    context = {
        "orders": zip(order_ids, order_status, order_collect, totals),
        "title": "Shop: My Orders",
    }

    print (order_ids)

    return render(request, "my-orders.html", context)
    