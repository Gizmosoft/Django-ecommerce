from django.shortcuts import render

from .models import Cart
# Create your views here.

def cart_create():
    cart_obj = Cart.objects.create(user=None)
    print('New cart created!')
    return cart_obj

## We want the cart views to be only visible to the logged in customers
## We would use Django Sessions to do that
## Session object is on the request object by default
def cart_home(request):
    #del request.session['cart_id']      # delete the previous session id
    #request.session['cart_id'] = "12"   # setting cart id as a test
    cart_id = request.session.get("cart_id", None)  # get current cart ID or else show none
    # if cart_id is None and isinstance(cart_id, int):    # isinstance checks if the cart_id is of type integer
    #     cart_obj = cart_create()
    #     request.session['cart_id'] = cart_obj.id 
    # else:
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        cart_obj = qs.first()
        print("Cart ID exists...")
        # print(cart_id)
        # cart_obj = Cart.objects.get(id=cart_id)
        # print(cart_obj)
        ## below condition assigns an already created cart when user was not logged in to the user once they login
        if request.user.is_authenticated and cart_obj.user is None:
            cart_obj.user = request.user
            cart_obj.save()
    else:
        cart_obj = Cart.obj.new_cart(user=request.user)
        request.session['cart_id'] = cart_obj.id
    #print(request.session)
    #print(dir(request.session)) # helps us inspect the various method on the session module
    # key = request.session.session_key
    # print(key)
    # request.session['first_name'] = 'Kartikey' # Setter 
    # Doing something like below would not be possible as we cannot assign an object to a field in dictionary
    #request.session['xyz'] = request.user
    return render(request, "carts/home.html", {})