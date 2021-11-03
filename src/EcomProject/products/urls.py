from django.urls import path, re_path

from .views import (
                    ProductListView, 
                    ProductDetailSlugView,
                    )

urlpatterns = [
    path('', ProductListView.as_view()),     # making class based view as callable
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
]
