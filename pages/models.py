from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    customer = models.ForeignKey('Profile', on_delete=models.CASCADE)
    ordered_items = models.ManyToManyField('Item')
    address = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.customer.user.username



class Item(models.Model):
    id = models.AutoField(primary_key=True)  # Primary Key
    name = models.CharField(max_length=120)  # Item Name
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Item Price
    picture = models.ImageField(blank=True, null=True)  # Item Picture
    description = models.TextField(
        blank=True, max_length=430)  # Item Description
    stock = models.IntegerField(default=1)  # Number of the Item available

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
        if self.stock > 0:
            return True
        else:
            return False

    '''
    Returns the filepath for the item picture
    '''

    def get_image(self):
        return f'/static/items/{self.picture}'


class Address(models.Model):
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length = 15, blank=True)
    zip_code = models.CharField(max_length=8, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addresses = models.ManyToManyField(
         'Address', 
         through='AddressInfo',
         through_fields=('profile', 'address')
    )
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


class AddressInfo(models.Model):

    HOME_ADDRESS = 1
    SHIPPING_ADDRESS = 2

    TYPE_ADDRESS_CHOICES = (
        (HOME_ADDRESS, "Home address"),
        (SHIPPING_ADDRESS, "Shipping address"),
    )

    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    # This is the field you would use for know the type of address.
    address_type = models.PositiveIntegerField(choices=TYPE_ADDRESS_CHOICES)