from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Marca
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ContactForm
from django import forms
from django.db.models import Q




def search(request):
    # Preparar los filtros seleccionados
    products = Product.objects.all()
    categories = Category.objects.all()
    marcas = Marca.objects.all()

    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    marca_filter = request.GET.get('marca', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Filtrado avanzado de acuerdo con los parámetros enviados por el usuario
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_filter:
        products = products.filter(category__id=category_filter)
    if marca_filter:
        products = products.filter(marca__id=marca_filter)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if not products:
        messages.error(request, "No se encontraron productos para tu búsqueda.")
    return render(request, "search.html", {
        'products': products,
        'query': query,
        'categories': categories,
        'marcas': marcas,
    })



def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            messages.error(request, "Profile does not exist for the current user.")
            return redirect('home')  # O redirigir a otra página

        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated.")
            return redirect('home')
        return render(request, "update_info.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('home')




def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #did they fill oput the form 
        if request.method == 'POST':
            #Do stuff
            form = UpdateUserForm(current_user, request.POST)
            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "your password has been updated, please log in again...")
                #login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "You must be logget in to view that page. ")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has Been Updated")
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You must be logged in to acces ")
        return redirect('homee')



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def category(request, foo):
    #remplace gyphens with Space
    foo = foo.replace('-', ' ')
    #Grab the category from the url 
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter( category=category)
        return render(request, 'category.html', {'products': products, 'category':category})

    except:
        messages.success(request, ("that Category Doesnt Exist"))
        return redirect('homen')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()  # Obteniendo todas las categorías
    return render(request, 'home.html', {'products': products, 'categories': categories})



def about(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out! We will get back to you soon.")
            return redirect("about")
    else:
        form = ContactForm()
    return render(request, "about.html", {"form": form})



def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("you have been logged"))
            return redirect('home')
        else:
            messages.success(request, ("There was a erro please try again"))
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('home')


def register_user(request):

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username created please full out you user infomation"))
            return redirect('update_info')
        else:
            messages.success(request, ("there was a problem please train again "))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form':form})