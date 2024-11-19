from django.contrib import admin
from .models import Category, Marca, Customer, Product, ProductImage, Order, Profile, ContactMessage
from django.contrib.auth.models import User

# Registro de modelos
admin.site.register(Category)
admin.site.register(Marca)
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(Order)

# Mezclar perfil de usuario
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Reemplazar registro de User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")

# Incluir imágenes adicionales para los productos
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Campos adicionales para cargar imágenes

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'marca', 'is_sale')
    inlines = [ProductImageInline]

# Registrar Product con configuración personalizada
admin.site.register(Product, ProductAdmin)
