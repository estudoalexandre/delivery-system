# storefront/context_processors.py

from .models import Cart, CartProduct

def cart_products_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_products = CartProduct.objects.filter(cart=cart)
    else:
        cart_products = []


    return {'cart_products': cart_products}

