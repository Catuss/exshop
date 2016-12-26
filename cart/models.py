from django.db import models
from catalog.models import Good

class CartItem(models.Model):

    class Meta:
        ordering = ['cart_date']
    cart_id = models.CharField(max_length=50)
    cart_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    good = models.ForeignKey(Good, unique=False)

    def name(self):
        return self.good.name

    def augment_quantity(self, quantity):
         self.quantity = self.quantity + int(quantity)
         self.save()


class Order(models.Model):

    order_location = models.CharField(max_length=200)
    order_name = models.CharField(max_length=200)
    order_email = models.EmailField()
    order_phone_number = models.CharField(max_length=20)
    order_good_id = models.CharField(max_length=20)