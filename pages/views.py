from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.forms import SignUpForm, ReviewForm
import operator
# import for the models needed
from .models import CartDetails, Profile, Item, Address, Review, Order, OrderDetails

""" 
Profile page
Require users to login to view this page, redirect if not. 
"""


@login_required(login_url='/accounts/login/')
def profile_view(request, *args, **kwargs):
    address = Address.objects.get(user=request.user.profile)
    context = {
        "address": address,
        "title": "Shop: My Profile"
    }
    return render(request, "profile.html", context)


""" 
About the website view
"""


def about_view(request):
    return render(request, "about-us.html", {})


""" 
Main/home page that displays the items on sale.
"""


def index(request, *args, **kwargs):

    # If sort request is received from user
    if request.method == 'GET' and 'filter' in request.GET:
        print('Request made.')
        filter_req = request.GET['filter']
        all_items = Item.objects.order_by(filter_req)

    # No sort then sort by default alphabetical
    else:
        all_items = Item.objects.order_by("name")

    context = {
        'all_items': all_items,
        'title': 'Shop'
    }

    return render(request, "home.html", context)


""" 
Signup page for new users. Displays the SignUp form and
creates new users when a valid form is submitted.
"""


def signup(request):

    # If a form is submitted
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # Adding the address inputs
            address = Address.objects.create(
                user=user.profile,
                address_line_1=form.cleaned_data.get('address_line_1'),
                address_line_2=form.cleaned_data.get('address_line_2'),
                city=form.cleaned_data.get('city'),
                country=form.cleaned_data.get('country'),
                zip_code=form.cleaned_data.get('zip_code'),
            )
            # Save the birthdate
            user.profile.birth_date = form.cleaned_data.get("birth_date")
            address.save()
            user.save()

            raw_password = form.cleaned_data.get('password1')

            # Login the new user
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')

    # If a form has not yet been submitted, then display an empty form
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


""" 
Add items to cart.
"""


@login_required(login_url='/accounts/login/')
def add_cart(request, item_id):

    item = Item.objects.get(item_id=item_id)  # retreive item from database
    cart, cart_created = CartDetails.objects.get_or_create(
        item=item, user=request.user)  # get or create a cart for the user

    # if a new cart was not created then increment the quantity
    if not cart_created:
        cart.quantity += 1
        cart.save()

    return redirect('/my-cart')


""" 
View all items in cart
"""


@login_required(login_url='/accounts/login/')
def cart_view(request):

    # check if a cart for the user exists
    if CartDetails.objects.filter(user=request.user).exists():
        cart = CartDetails.objects.filter(
            user=request.user)  # lll the user's carts

        cart_items = []  # list of items
        quantity = []  # list of corresponding quantities for the items
        subtotal = []  # list of corresponding subtotals for the items

        # Go through each item in the collection of carts and append to the lists
        for cart_item in cart:
            cart_items.append(cart_item.item)
            quantity.append(cart_item.quantity)
            subtotal.append(cart_item.item.price * cart_item.quantity)

        # Zip the lists to pass to frontend
        cart_quantity = zip(cart_items, quantity, subtotal)

        context = {
            'cart': cart_quantity,
            'total': sum(subtotal),
            'title': 'Shop: My Cart'
        }

    # If no cart exists
    else:
        context = {
            'title': 'Shop: My Cart'
        }

    return render(request, "cart.html", context)


""" 
A page for viewing a single item and passing the item details and reviews
"""


def item_view(request, item_id):
    item = Item.objects.get(item_id=item_id)  # get the item by the item_id

    # Check if there are reviews available for the item.
    if Review.objects.filter(item=item).exists():
        reviews = Review.objects.filter(item=item)

        context = {
            "item": item,
            "reviews": reviews,
            "title": item.name
        }

    # If there are no reviews
    else:
        context = {
            "item": item,
            "title": item.name
        }

    return render(request, "item.html", context)


""" 
Remove an item from user's cart
"""


@login_required(login_url='/accounts/login/')
def remove_item(request, item_id):
    item = Item.objects.get(item_id=item_id)  # get the item

    cart = CartDetails.objects.get(
        user=request.user, item=item)  # get the cart

    # If only one of the item is in the cart then delete the cart
    if cart.quantity == 1:
        cart.delete()

    # Else more than one then decrement
    else:
        cart.quantity -= 1
        cart.save()

    return redirect('/my-cart')


""" 
View for the confirmation checkout page
"""


@login_required(login_url='/accounts/login/')
def checkout_view(request):
    order = Order.objects.create(
        user=request.user.profile)  # Create a new order
    cart = CartDetails.objects.filter(
        user=request.user)  # Get the current user's cart

    order_details = []  # List for each item/order_details
    subtotals = []  # Subtotal for each item/order_detail

    # Go through each item in the cart and create order_details for each.
    # and append the details to the list for the frontend
    for item_cart in cart:
        order_item = OrderDetails.objects.create(
            order_id=order,
            item=item_cart.item,
            quantity=item_cart.quantity,
        )
        subtotals.append(item_cart.item.price * item_cart.quantity)
        order_details.append(order_item)

    # Zip for frontend
    order_subtotal = zip(order_details, subtotals)

    # Delete the cart since checkout
    cart.delete()

    context = {
        "order_num": order.order_id,
        "order": order_subtotal,
        "total": sum(subtotals),
        "title": f"Order no: {order.order_id}",
    }

    return render(request, "checkout.html", context)


""" 
View for all the user's orders
"""


@login_required(login_url='/accounts/login/')
def orders_view(request):
    all_orders = Order.objects.filter(
        user=request.user.profile).order_by('-created_date')  # Get all the orders sorted by recency

    order_ids = []  # List for Order IDs
    order_status = []  # List for Order Status
    order_collect = []  # Lists of Order Details for each order (list of lists)
    totals = []  # Totals for each order

    # Get each order_detail in all the user's orders
    for orders in all_orders:
        order_ids.append(orders.order_id)  # Append order_id
        order_status.append(orders.get_status)  # Append order status
        # Get all the order_details under this order_id
        order = OrderDetails.objects.filter(order_id=orders.order_id)

        single_order = []  # List for all the order_details
        total_order = 0  # Total for the order

        # Go through each item in the order and append
        for item in order:
            single_order.append(item)
            total_order += int(item.get_subtotal())

        order_collect.append(single_order)
        totals.append(total_order)

    context = {
        "orders": zip(order_ids, order_status, order_collect, totals),
        "title": "Shop: My Orders",
    }

    return render(request, "my-orders.html", context)


""" 
View for submitting reviews
"""


@login_required(login_url='/accounts/login/')
def review_view(request, item_id):
    item = Item.objects.get(item_id=item_id)

    # If a submission is made, check validity and make changes to database
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user_review, _ = Review.objects.get_or_create(
                item=item, user=request.user)
            item_rating = form.cleaned_data.get("item_rating")
            review_text = form.cleaned_data.get("review_text")
            user_review.update_review(item_rating, review_text)

            return redirect(f'/item/{item_id}')

    # If not a submission then send an empty form to be filled up
    else:
        form = ReviewForm()
        context = {
            "review_form": form,
            "item": item,
            "title": "Shop: Review item"
        }

    return render(request, "review-item.html", context)
