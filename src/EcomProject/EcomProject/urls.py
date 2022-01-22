"""EcomProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

# from products.views import (ProductListView, 
#                             product_list_view,
#                             ProductDetailView,
#                             ProductDetailSlugView,
#                             product_detail_view,
#                             ProductFeaturedDetailedView
#                             )
from .views import home_page, about_page, contact_page, login_page, register_page, logout_operation

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('products/', include(("products.urls", 'products'), namespace='products')),
    path('search/', include(("search.urls", 'search'), namespace='search')),
    # re_path(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailedView.as_view()),
    # path('products-class/', ProductListView.as_view()),     # making class based view as callable
    # path('products-function/', product_list_view),
    # re_path(r'^products-class/(?P<pk>\d+)/$', ProductDetailView.as_view()),     # making class based view as callable
    # re_path(r'^products-class/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
    # re_path(r'^products-function/(?P<pk>\d+)/$', product_detail_view),
    path('logout/', logout_operation, name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)