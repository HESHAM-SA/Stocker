from django.db import models

# Create your models here.


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='supplier_logos/', default='supplier_logos/default_logo.svg', null=True, blank=True )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.supplier_name

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    suppliers = models.ManyToManyField(Supplier)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    description  = models.TextField(blank=True)


    def __str__(self):
        return self.product_name