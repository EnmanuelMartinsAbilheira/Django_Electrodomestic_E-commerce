from django.contrib import admin
from .models import Category, Marca, Customer, Product, Order, Profile, ContactMessage
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Category)
admin.site.register(Marca)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)


#Mix profile into and user info 
class ProfileInline(admin.StackedInline):
    model = Profile


#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


# Unregister the old way
admin.site.unregister(User)

# re-register the new way 
admin.site.register(User, UserAdmin)




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")
