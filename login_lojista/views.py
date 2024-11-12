from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import LojistaRegistrationForm, EmailAuthenticationForm
from delivery_store.models import Store
from django.contrib.auth.models import User



class LojistaLoginView(auth_views.LoginView):
    template_name = 'login_lojista/login.html'
    redirect_authenticated_user = False  
    authentication_form = EmailAuthenticationForm
    success_url = reverse_lazy('delivery_store:index')
    
    
    def get_success_url(self):
        return self.success_url

class LojistaLogoutView(auth_views.LogoutView):
    template_name = 'login_lojista/logged_out.html'

def register_lojista(request):
    if request.method == "POST":
        form = LojistaRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('login_lojista:login')
            except IntegrityError:
                form.add_error('email', 'Email já cadastrado')
    else:
        form = LojistaRegistrationForm()
    return render(request, 'login_lojista/register.html', {'form': form})

def profile_lojista(request):
    store = get_object_or_404(Store, owner=request.user)
    return render(request, 'login_lojista/profile.html', {
        'store': store})


