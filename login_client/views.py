from django.shortcuts import render, redirect, get_object_or_404
from .models import UserClientProfile, UserClientAdresses
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .forms import ClientRegistrationForm, ClientUpdateForm, UserClientAdressesForm
from django.urls import reverse_lazy
from storefront.utils import transfer_session_cart_to_user


def check_email_exists(request):
    email = request.GET.get('email')
    if User.objects.filter(email=email).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})

def register_client(request):
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data.get('name')
            name_parts = full_name.split(maxsplit=1)
            
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()
             
            login(request, user)
            transfer_session_cart_to_user(request)

            client_profile, created = UserClientProfile.objects.get_or_create(user=user)
            client_profile.phone = form.cleaned_data.get('phone')
            client_profile.cpf = form.cleaned_data.get('cpf')
            client_profile.birthday = form.cleaned_data.get('birthday')
            client_profile.save()

            return JsonResponse({"success": True, "message": "Conta criada com sucesso!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        return JsonResponse({"success": False, "message": "Método inválido"}, status=405)
    

class CustomLoginView(LoginView):
    template_name = 'storefront/base_storeview.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('storefront:index')
    
    def form_invalid(self, form):
        redirect_url = self.get_success_url()
        print("Redirect URL no Django (form_valid):", redirect_url)  
        response = super().form_invalid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        else:
            return response
        
    def form_valid(self, form):
        self.object = form.get_user()
        login(self.request, self.object)

        transfer_session_cart_to_user(self.request)

        redirect_url = self.get_success_url()
        print("Redirect URL no Django (form_valid):", redirect_url)  

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "redirect_url": redirect_url})
        else:
            return super().form_valid(form)

def update_client(request, client_id):
    client = get_object_or_404(User, pk=client_id)
    
    if request.method == "POST":
        form = ClientUpdateForm(request.POST, instance=client)
        
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data.get('name')
            name_parts = full_name.split(maxsplit=1)
            
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()
            
            # Atualizar ou criar o perfil do cliente
            user_client, created = UserClientProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': form.cleaned_data.get('phone'),
                    'cpf': form.cleaned_data.get('cpf'),
                    'birthday': form.cleaned_data.get('birthday'),
                }
            )
            
            return render(request, 'login_client/update_client.html', {
                'form': form, 'client': client, 'success': True
            })
    else:
        form = ClientUpdateForm(instance=client)
    
    return render(request, 'login_client/update_client.html', {
        'form': form, 'client': client
    })
    
def save_address(request, slug):
    
    if request.method == 'POST':
        print(request.POST)
        form = UserClientAdressesForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('storefront:index', slug=slug)
        else:
            print(form.errors)
    else:
        form = UserClientAdressesForm()
    return render(request, 'storefront/index.html', {
        'form': form,
        'slug': slug})




# Create your views here.
