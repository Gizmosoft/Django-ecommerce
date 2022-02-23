from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product
# Create your views here.

## The logic of the below method has been moved to models.py
# def cart_create():
#     cart_obj = Cart.objects.create(user=None)
#     print('New cart created!')
#     return cart_obj

## We want the cart views to be only visible to the logged in customers
## We would use Django Sessions to do that
## Session object is on the request object by default
def cart_home(request):
    cart_obj, new_obj = Cart.obj.new_or_get(request)

## Below is a very simple and inefficient way of calculating cart total price
    # products = cart_obj.product.all()
    # total = 0
    # # Calculate total cart price
    # for p in products:
    #     total += p.price
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product does not exist anymore!")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.obj.new_or_get(request)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_obj)
        else:
            cart_obj.product.add(product_obj)   # or --> cart_obj.product.add(product_id) | The addition of the new product obj happens in the models.py where we have called m2m_changed()
        request.session['cart_items_count'] = cart_obj.product.count()    # counts the total number of products in cart
    return redirect("cart:home")


# All the lines/snippets marked with --> have been moved to the CartManager model simplifying the views.
    #del request.session['cart_id']      # delete the previous session id
    #request.session['cart_id'] = "12"   # setting cart id as a test
    #--> cart_id = request.session.get("cart_id", None)  # get current cart ID or else show none
    # if cart_id is None and isinstance(cart_id, int):    # isinstance checks if the cart_id is of type integer
    #     cart_obj = cart_create()
    #     request.session['cart_id'] = cart_obj.id 
    # else:
    #--> qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     cart_obj = qs.first()
    #-->     print("Cart ID exists...")
        # print(cart_id)
        # cart_obj = Cart.objects.get(id=cart_id)
        # print(cart_obj)
        ## below condition assigns an already created cart when user was not logged in to the user once they login
    #-->     if request.user.is_authenticated and cart_obj.user is None:
    #         cart_obj.user = request.user
    #-->         cart_obj.save()
    #--> else:
    #     cart_obj = Cart.obj.new_cart(user=request.user)
    #-->     request.session['cart_id'] = cart_obj.id
    #print(request.session)
    #print(dir(request.session)) # helps us inspect the various method on the session module
    # key = request.session.session_key
    # print(key)
    # request.session['first_name'] = 'Kartikey' # Setter 
    # Doing something like below would not be possible as we cannot assign an object to a field in dictionary
    #request.session['xyz'] = request.user
    return render(request, "carts/home.html", {})