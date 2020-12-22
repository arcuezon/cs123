from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    picture = models.ImageField(blank = True, null = True)
    description = models.TextField(blank=True, max_length=430)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def in_stock(self):
        if self.stock > 0:
            return True
        else:
            return False

    def get_image(self):
        return f'/static/items/{self.picture}'