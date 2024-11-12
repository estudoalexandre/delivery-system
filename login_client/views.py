from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .forms import ClientRegistrationForm
from django.urls import reverse_lazy
from storefront.utils import transfer_session_cart_to_user


def check_email_exists(request):
    email = request.GET.get('email')
    if User.objects.filter(email=email).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})

def register_client(request):
    if request.method == "POST":
        print("Requisição POST recebida :", request.POST)  # Log para depuração
        form = ClientRegistrationForm(request.POST)
        print("Formulário válido", form)  # Log para depuração
        if form.is_valid():
            user = form.save()  # O formulário já lida com a associação ao grupo "Cliente"
            print("Usuário criado:", user)  # Log para depuração
            login(request, user)
            transfer_session_cart_to_user(request)
            return JsonResponse({"success": True, "message": "Conta criada com sucesso!"})
        else:
            # Retornar erros de validação como JSON
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        return JsonResponse({"success": False, "message": "Método inválido"}, status=405)
    

class CustomLoginView(LoginView):
    template_name = 'storefront/base_storeview.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Prioriza o 'next' passado no POST e, em seguida, tenta no GET
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        print("Next URL no Django:", next_url)  # Log para depuração
        # Retorna o 'next_url' ou uma URL padrão se for None
        return next_url if next_url else reverse_lazy('storefront:index')
    
    def form_invalid(self, form):
        redirect_url = self.get_success_url()
        print("Redirect URL no Django (form_valid):", redirect_url)  # Log adicional para depuração
        response = super().form_invalid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        else:
            return response
        
    def form_valid(self, form):
        # Executa o login do usuário
        self.object = form.get_user()
        login(self.request, self.object)

        # Transfere o carrinho da sessão para o usuário autenticado
        transfer_session_cart_to_user(self.request)

        # Obtenha a URL de redirecionamento
        redirect_url = self.get_success_url()
        print("Redirect URL no Django (form_valid):", redirect_url)  # Log adicional para depuração

        # Verifica se é uma requisição AJAX e retorna JSON se for o caso
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "redirect_url": redirect_url})
        else:
            return super().form_valid(form)




# Create your views here.
