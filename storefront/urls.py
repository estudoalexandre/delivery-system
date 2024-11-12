from django.urls import path
from . import views

app_name = 'storefront'
urlpatterns = [
    path('<int:product_id>/', views.add_cart, name='add_cart'),
    path('<slug:slug>/', views.store_view, name='index'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('update/<int:product_id>/', views.update_cart_item, name='update_cart'),
]