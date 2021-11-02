from django.contrib import admin
from django.db.models.base import Model

# Register your models here.
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)