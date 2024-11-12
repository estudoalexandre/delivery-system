from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'login_client'
urlpatterns = [
    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
    path('login/', views.CustomLoginView.as_view(), name='login_client'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_client'),
    path('register_client/', views.register_client, name='register_client'),
    

]