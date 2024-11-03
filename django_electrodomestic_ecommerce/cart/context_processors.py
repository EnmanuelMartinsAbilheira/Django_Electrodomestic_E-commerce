from .cart import Cart

#Create Context processor so our cart can work on all pages of the site
def cart(request):
    #return the default data form our Cart
    return {'cart': Cart(request)}
