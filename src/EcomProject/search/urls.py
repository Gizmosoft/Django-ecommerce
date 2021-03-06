from django.urls import path, re_path
from django.views.generic import detail

from products.views import (
                    ProductListView, 
                    ProductDetailSlugView,
                    )

from .views import SearchProductView

urlpatterns = [
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),

    path('', SearchProductView.as_view(), name='query'),
]
