from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Store, Categoria, Product
from django.http import JsonResponse
from .forms import StoreForm, CategoryProductForm, ProductForm
# Create your views here.

def index(request):
    
    if not request.user.groups.filter(name='Lojista').exists():
        return render(request, 'forbidden.html', status=403)    
    
    return render(request, 'delivery_store/index.html')


@login_required
def create_or_update_store(request):
    
    if not request.user.groups.filter(name='Lojista').exists():
        return render(request, 'forbidden.html', status=403)
    
    store = Store.objects.filter(owner=request.user).first()
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            return redirect('delivery_store:index')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = StoreForm(instance=store)
    
    return render(request, 'delivery_store/create_store.html', {'form': form})

def delete_store(request):
    store = Store.objects.filter(owner=request.user).first()
    if store:
        store.delete()
    return redirect('delivery_store:index')

def add_category(request):
    if request.method == "POST":
        form = CategoryProductForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.owner = request.user
            categoria.store = Store.objects.get(owner=request.user)
            categoria.save()
            return redirect('delivery_store:menu')
        else:
            print("Erros no formulário:", form.errors)
    else:
        form = CategoryProductForm()
        
    return render(request, 'delivery_store/menu.html', {'form': form})

def update_category(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoryProductForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('delivery_store:menu')
        else:
            print("Erros no formulário:", form.errors)
    else:
        form = CategoryProductForm(instance=categoria)
    
    return render(request, 'delivery_store/menu.html', {
        'form': form,
        'categoria': categoria})
    
def delete_category(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('delivery_store:menu')
    return render(request, 'delivery_store/index.html', {
        'categoria': categoria})
    

            
@login_required
def menu_catalog(request):
    
    if not request.user.groups.filter(name='Lojista').exists():
        return render(request, 'forbidden.html', status=403)
    
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return redirect('delivery_store:create_or_update_store')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Obtém o ID da categoria a partir do formulário
            categoria_id = request.POST.get('categoria_id')
            if not categoria_id:
                form.add_error(None, "Categoria não selecionada.")
                return render(request, 'delivery_store/menu.html', {
                    'store': store,
                    'categories_with_products': categories_with_products,
                    'form': form,
                })

            categoria = get_object_or_404(Categoria, id=categoria_id, store=store)
            product.categoria = categoria
            product.owner = request.user
            product.store = store
            product.save()
            return redirect('delivery_store:menu')
    else:
        form = ProductForm()

    categories = Categoria.objects.filter(store=store)
    categories_with_products = [
        {'categoria': cat, 'products': cat.products.all()}
        for cat in categories
    ]

    return render(request, 'delivery_store/menu.html', {
        'store': store,
        'categories_with_products': categories_with_products,
        'form': form,
    })

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('delivery_store:menu')
        else:
            print("Erros no formulário:", form.errors) 
            print(form.non_field_errors)
    else:
        form = ProductForm(instance=product)

    return render(request, 'delivery_store/menu.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('delivery_store:menu')
    return render(request, 'delivery_store/menu.html', {'product': product})


    

    