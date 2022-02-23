from operator import mod
from pyexpat import model
from django.db import models

from carts.models import Cart

# creating order choices
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

# Create your models here.
class Order(models.Model):
    order_id        = models.CharField(max_length=120, blank=True)  # Set of specific characters for tracking 😊
    # billing_profile = ?
    # shipping_address
    # billing_address
    cart            = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status          = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    # might depend on the geographic location 😨
    shipping_total  = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

# generate order id
# generate order total