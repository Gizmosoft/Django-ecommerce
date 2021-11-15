import os
import random

from django.db import models
from django.db.models.signals import pre_save # to do some operation just before saving to DB
from .utils import unique_slug_generator
from django.urls import reverse

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1000, 999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

# Creating custom Model Manager
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

# Create your models here. -> defines how we are connecting our Django app to a database
class Product(models.Model):
    title       = models.CharField(max_length=100)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    # saves each product with its title as name
    def __str__(self):  
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, Product)