from django.http import request
from django.shortcuts import render

from django.shortcuts import render 
from products.models import Product
from django.views.generic import ListView

# Create your views here.
class SearchProductView(ListView):
    template_name = "product/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.featured()