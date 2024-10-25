from django.contrib import admin
from .models import Category, Marca, Customer, Product, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Marca)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)