from django.http import request
from django.shortcuts import render

from django.shortcuts import render 
from products.models import Product
from django.views.generic import ListView

# Create your views here.
class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.featured()