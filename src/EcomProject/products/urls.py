from django.urls import path, re_path
from django.views.generic import detail

from .views import (
                    ProductListView, 
                    ProductDetailSlugView,
                    ) 
app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),     # making class based view as callable
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]
