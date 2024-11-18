from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'login_client'
urlpatterns = [
    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
    path('login/', views.CustomLoginView.as_view(), name='login_client'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_client'),
    path('register_client/', views.register_client, name='register_client'),
    path('update_client/<int:client_id>/', views.update_client, name='update_client'),
    path('<slug:slug>/save_address/', views.save_address, name='save_address'),
    

]