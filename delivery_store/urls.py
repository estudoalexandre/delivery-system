from django.urls import path
from . import views

app_name = 'delivery_store'

urlpatterns = [
    # Add your URL patterns here
    # Example:
    path('index/', views.index, name='index'),
    path('delete/', views.delete_store, name='delete'),
    path('add_category', views.add_category, name='add_category'),
    path('update_category/<int:categoria_id>/', views.update_category, name='update_category'),
    path('delete_category/<int:categoria_id>/', views.delete_category, name='delete_category'),
    path('create_or_update_store/', views.create_or_update_store, name='create_or_update_store'),
    path('menu/', views.menu_catalog, name='menu'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

]