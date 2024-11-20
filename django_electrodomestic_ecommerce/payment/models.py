from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)


    #dont pluralize address
    class Meta: 
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    

#create a user Shipping address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created: 
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

#automate the profile thing 
post_save.connect(create_shipping, sender=User)
    

#create order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    shipping_method = models.CharField( # metodo de envio 
        max_length=50,
        choices=[
            ('store_pickup', 'Recoger en tienda'),
            ('home_delivery', 'Entrega a domicilio')
        ],
        default='store_pickup'
    )
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def calculate_shipping_cost(self): #valor metodo de envio 
        """Calcula el costo de envío según el método seleccionado."""
        if self.shipping_method == 'home_delivery':
            return 15  # Costo fijo
        return 0  # Gratis para recoger en tienda

    def save(self, *args, **kwargs):
        self.shipping_cost = self.calculate_shipping_cost()
        self.final_total = self.amount_paid + self.shipping_cost
        super().save(*args, **kwargs)
    

# auto add shipping date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now









#create order items model 
class OrderItem(models.Model):
    #foreing keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'