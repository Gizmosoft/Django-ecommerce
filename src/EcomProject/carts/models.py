from django.conf import settings
from django.db import models

from products.models import Product

User = settings.AUTH_USER_MODEL     #importing user: this will go by the default user model in the settings or any customized user model that we might have created

# Create your models here.
class CartManager(models.Model):
    def new_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return Cart.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING) # Making sure, even the not logged in user can built a cart
    product     = models.ManyToManyField(Product, blank=True)   # allowing us to have a blank cart
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)   # shows when the cart was updated
    timestamp   = models.DateTimeField(auto_now_add=True)   # shows when the cart was created

    obj = CartManager()
    def __str__(self):
        return str(self.id)     # returns ID of the cart