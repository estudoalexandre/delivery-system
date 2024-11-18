from django.shortcuts import render, get_object_or_404, redirect
from delivery_store.models import Store, Product
from django.db.models import Sum
from .models import Cart, CartProduct
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
# Create your views here.


def store_view(request, slug):
    store = get_object_or_404(Store, slug=slug)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_products = CartProduct.objects.filter(cart=cart)
        total_price = sum(cart_product.product.price * cart_product.quantity for cart_product in cart_products)
    else:
        cart = request.session.get('cart', {})
        cart_products = [
            {
                'product': {
                    'id': product_id,
                    'name': item['name'],
                    'price': item['price'],
                    'image_url': item['image_url'],
                },
                'quantity': item['quantity']
            }
            for product_id, item in cart.items()
        ]
        total_price = sum([item['price'] * item['quantity'] for item in cart.values()])
    
    categories_with_products = [
        {'categoria': cat, 'products': cat.products.all()}
        for cat in store.categoria_set.all()
    ]
    
    context = {
        'store': store,
        'cart': cart,
        'cart_products': cart_products,
        'categories_with_products': categories_with_products,
        'total_price': total_price  # Agora `total_price` é sempre definido
    }
    
    return render(request, 'storefront/store_detail.html', context)


def add_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST['quantity'])
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=request.user,
                completed=False
            )
            cart.add_product(product, quantity)
        else:
            cart = request.session.get('cart', {})
            
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] += quantity
            else:
                cart[str(product_id)] = {
                    'name': product.name,
                    'price': float(product.price),
                    'quantity': quantity,
                    'image_url': product.image.url
                }
            request.session['cart'] = cart
            
        return redirect(reverse('storefront:index', args=(product.store.slug,)))
    
    return redirect('storefront:index')




def update_cart_item(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST['quantity'])
        
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user, completed=False)
                cart_product = CartProduct.objects.get(cart=cart, product=product)
                cart_product.quantity = quantity
                cart_product.save()
                messages.success(request, f'Quantidade de {product.name} atualizada com sucesso.')
                return redirect('storefront:index', slug=product.store.slug)
            
            except CartProduct.DoesNotExist:
                messages.error(request, f'Produto não encontrado no Carrinho')
            
            except Cart.DoesNotExist:
                messages.error(request, f'Carrinho nao encontrado')
            
            except ValueError:
                messages.error(request, f'Quantidade inválida')
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] = quantity
                request.session['cart'] = cart
                messages.success(request, f'Quantidade de {product.name} atualizada com sucesso.')
            else:
                messages.error(request, f'Produto não encontrado no Carrinho')
                
            return redirect('storefront:index', slug=product.store.slug)

    
        


def remove_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user, completed=False)
                cart_product = CartProduct.objects.get(cart=cart, product=product)
                cart_product.delete()
                messages.success(request, f'{product.name} Removido com sucesso.')
                return redirect('storefront:index', slug=product.store.slug)
            
            except CartProduct.DoesNotExist:
                messages.error(request, f'Produto não encontrado no Carrinho')
            
            except Cart.DoesNotExist:
                messages.error(request, f'Carrinho nao encontrado')
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart
                messages.success(request, f'{product.name} Removido com sucesso.')
            else:
                messages.error(request, f'Produto não encontrado no Carrinho')
        
            return redirect('storefront:index', slug=product.store.slug)
            

def cart_item_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        total_quantity = cart.cartproduct_set.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        return {'cart_item_count': total_quantity}
    else:
        cart = request.session.get('cart', {})
        if cart:
            total_quantity = sum([item['quantity'] for item in cart.values()])
            return {'cart_item_count': total_quantity}
    return {'cart_item_count': 0}

def get_cart_items(request, slug):
    store =  get_object_or_404(Store, slug=slug)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_products = cart.cartproduct_set.all()
    else:
        cart = request.session.get('cart', {})
        cart_products = [
            {
                'product': {
                    'id': product_id,
                    'name': item['name'],
                    'price': item['price'],
                    'image_url': item['image_url'],
                },
                'quantity': item['quantity']
            }
            for product_id, item in cart.items()
        ]
    return render(request, 'storefront/cart_items.html', {
        'cart_products': cart_products, 
        'store': store})
        


