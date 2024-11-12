from django.urls import path
from django.urls import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'login_lojista'

urlpatterns = [
    path('login/', views.LojistaLoginView.as_view(), name='login'),
    path('logout/', views.LojistaLogoutView.as_view(), name='logout'),
    path('register/', views.register_lojista, name='register'),
    path('profile/', views.profile_lojista, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('login_lojista:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('login_lojista:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('teste/', views.teste_view, name='teste'),
    # path('logout/', views.logout_view, name='logout'),
]