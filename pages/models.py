from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
#python manage.py graph_models -a > my_project.dot

'''
Extends the base user model and allows adding of address and cart
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("Profile", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, default = "H")
    #Address information
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length = 15, blank=True)
    zip_code = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return f"{self.user.user.username}: {self.get_type()}"

    def get_type(self):
        if self.address_type == 'H':
            return 'Home'
        elif self.address_type == 'W':
            return 'Work'
        else:
            return 'Temporary'

    def set_type(self, address_type):
        if address_type == 'Home':
            self.address_type = 'H'
        elif address_type == 'Work':
            self.address_type = 'Work'
        else:
            self.address_type = 'A'


class CartDetails(models.Model):
    cart_detail_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}: {self.item.item_id}"

    def get_quantity(self):
        return self.quantity

    def get_subtotal(self):
        subtotal = self.item.price * self.quantity
        return subtotal


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)  # Primary Key
    name = models.CharField(max_length=120)  # Item Name
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Item Price
    description = models.TextField(
        blank=True, max_length=430)  # Item Description
    quantity_stock = models.IntegerField(default = 1)
    quantity_order = models.IntegerField(default = 0)
    picture = models.ImageField(blank=True, null=True)  # Item Picture

    '''
    Method to display human readable field instead of
    the non-descriptive ID primary key
    '''
    def __str__(self):
        return self.name

    '''
    Returns a boolean depending on the availble supply
    of the item.
    '''
    def in_stock(self):
        stock = self.quantity_stock - self.quantity_order
        if stock > 0:
            return 'In stock'
        else:
            return 'Out of stock'

    '''
    Returns the filepath for the item picture
    '''
    def get_image(self):
        return f'/static/items/{self.picture}'


class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    user = models.ForeignKey("Profile", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default = 'P')
    created_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user.user.username}: {str(self.created_date)[0:19]}"

    def get_status(self):
        if self.status == 'P':
            return 'Processing'
        elif self.status == 'S':
            return 'Shipped'
        elif self.status == 'D':
            return 'Delivered'
        else:
            return 'Invalid status'
    
    
class OrderDetails(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default = 1)

    def __str__(self):
        return f"Order no. {self.order_id.order_id}:  {self.item.item_id}"

    def get_subtotal(self):
        subtotal = self.item.price * self.quantity
        return subtotal


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=5)
    review_text = models.TextField(blank=True)

