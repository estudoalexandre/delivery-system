from .models import Cart
from delivery_store.models import Product

def transfer_session_cart_to_user(request):
    if not request.user.is_authenticated:
        return
    
    # Obtenha o carrinho da sessão
    session_cart = request.session.get('cart', {})
    
    # Verifique se o usuário autenticado já tem um carrinho (se tiver, mescle os itens)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    
    for item_id, item_data in session_cart.items():
        # Obtenha o produto usando o item_id
        try:
            product = Product.objects.get(id=item_id)
            # Adicione o produto ao carrinho do usuário
            user_cart.add_product(product, item_data['quantity'])
        except Product.DoesNotExist:
            continue
    
    # Limpa o carrinho da sessão
    request.session['cart'] = {}
    request.session.modified = True
