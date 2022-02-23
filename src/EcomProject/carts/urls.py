from django.urls import path, re_path
from django.views.generic import detail

from .views import (
                    cart_home, 
                    cart_update,
                    ) 
app_name = 'carts'
urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
]
