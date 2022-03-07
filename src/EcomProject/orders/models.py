import math
from django.db.models.signals import pre_save, post_save
from django.db import models

from EcomProject.utils import unique_order_id_generator
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
    # This should be Random and Unique
    order_id        = models.CharField(max_length=120, blank=True)  # Set of specific characters for tracking 😊
    # billing_profile = ?
    # shipping_address
    # billing_address
    cart            = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status          = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    # might depend on the geographic location 😨 - press Win + . for emojis
    shipping_total  = models.DecimalField(default=50.00 , max_digits=100, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_new_total = format(new_total, '.2f')
        self.total = formatted_new_total
        self.save()
        return new_total

# generate order id
# generate order total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

# condition when cart is updated/saved
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

# condition when order is created
def post_save_order(sender, instance, created, *args, **kwargs):
    # below code updates the order
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)