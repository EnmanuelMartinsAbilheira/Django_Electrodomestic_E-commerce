from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, blank=True)
    subject = models.CharField(max_length=150)
    phone = models.CharField(max_length=10)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


#create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart  = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.user.username
    
#create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created: 
        user_profile = Profile(user=instance)
        user_profile.save()

#automate the profile thing 
post_save.connect(create_profile, sender=User)





# Create your models here.

#categories of products    
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 
    
    #@daverobb2011
    class Meta:
        verbose_name_plural = 'categories'
    
#marca of products    
class Marca(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 

#customers
class Customer(models.Model): 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



# all of our products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price= models.DecimalField(default=0, decimal_places=2, max_digits=6) #9999,99$
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/') # Main image
   
    #add sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price= models.DecimalField(default=0, decimal_places=2, max_digits=6) #9999,99$

    # Additional fields for appliance details
    energy_class = models.CharField(max_length=3, choices=[('A++', 'A++'), ('A+', 'A+'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')], blank=True)
    dimensions = models.CharField(max_length=50, help_text="Dimensions in cm (HxWxD)", blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in kg", blank=True, null=True)
    capacity = models.CharField(max_length=50, help_text="Capacity in liters or kg", blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    emisao_som = models.CharField(max_length=30, blank=True, null=True)

    # Codigo referencia producto 
    reference = models.CharField(max_length=30, help_text="Product reference", blank=True, null=True)
    ean = models.CharField(max_length=13, help_text="European Article Number (EAN)", blank=True, null=True)

    additional_info = models.TextField(blank=True, null=True)  # Información adicional
    more_info = models.TextField(blank=True, null=True)  # Texto para el nuevo colapsable


    
    def __str__(self):
        return self.name 
    

# New model for additional images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return f"Image for {self.product.name}"



# Customer Orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=150, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return self.product 