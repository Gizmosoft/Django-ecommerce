from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product

User = settings.AUTH_USER_MODEL     #importing user: this will go by the default user model in the settings or any customized user model that we might have created

# Create your models here.
class CartManager(models.Model):
    # the below method is a customized version of in built function "def get_or_create"
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = Cart.objects.filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False     # shows that new cart object is not created
            cart_obj = qs.first()
            print("Cart ID exists...")
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.obj.new_cart(user=request.user)
            new_obj = True      # Shows that new cart object is created
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return Cart.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING) # Making sure, even the not logged in user can built a cart
    product     = models.ManyToManyField(Product, blank=True)   # allowing us to have a blank cart
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)   # shows when the cart was updated
    timestamp   = models.DateTimeField(auto_now_add=True)   # shows when the cart was created

    obj = CartManager()
    def __str__(self):
        return str(self.id)     # returns ID of the cart


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    print(action)
    if (action=='post_add' or action=='post_remove' or action=='post_clear'):
        print(instance.product.all())
        print(instance.total)
        products = instance.product.all()
        total = 0
        # Calculate total cart price
        for p in products:
            total += p.price
        print(total)
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.product.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10 #* 1.18  # Adding Taxes
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)
