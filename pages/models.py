from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key = True) #Primary Key
    name = models.CharField(max_length = 120) #Item Name
    price = models.DecimalField(max_digits=6, decimal_places=2) #Item Price
    picture = models.ImageField(blank = True, null = True) #Item Picture
    description = models.TextField(blank=True, max_length=430) #Item Description
    stock = models.IntegerField(default=1) #Number of the Item available

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