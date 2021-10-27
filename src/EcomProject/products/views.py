from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404, request

# Create your views here.
from .models import Product

# class based View
class ProductListView(ListView):
    # queryset = modelclass.objects.function()
    queryset = Product.objects.all()        # get all data from DB
    template_name = "product/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

class ProductFeaturedDetailedView(DetailView):
    queryset = Product.objects.featured()
    template_name = "product/featured.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()

# function based view
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list' : queryset
    }
    return render(request, "product/list.html", context)

class ProductDetailView(DetailView):
    # queryset = modelclass.objects.function()
    queryset = Product.objects.all()        # get all data from DB
    template_name = "product/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


# function based view
def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk)     # id of particular object
    # instance = get_object_or_404(Product, pk=pk)

    # doing similar function as get_object_or_404() but we are handling our own error here below
    # try:
    #     instance = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     print("no product here")
    #     raise Http404("Product Does Not Exist!")

    # getting an instance of a custom model manager - by doing this, we are doing the below operation within the Models by customizing the model manager
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product Does Not Exist!")

    # Another way to do what we did above is by using queryset filters...
    # qs = Product.objects.filter(pk=pk)
    # print(qs)
    # if(qs.exists() and qs.count() == 1):
    #     instance = qs.first()
    # else:
    #     raise Http404("Product Does Not Exist!")

    context = {
        'object' : instance
    }
    return render(request, "product/detail.html", context)