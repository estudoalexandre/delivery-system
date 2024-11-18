from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User, UserClientAdresses

class ClientRegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Nome e Sobrenome', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Celular', required=False)
    cpf = forms.CharField(label='CPF', required=False)
    birthday = forms.DateField(label='Aniversário', required=False)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError('Por favor, informe seu nome completo.')
        return name
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if not password:
            raise ValidationError("O campo de senha é obrigatório.")
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('As senhas não conferem.')
        return confirm_password

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            client_group, created = Group.objects.get_or_create(name='Cliente')
            user.groups.add(client_group)
        return user


class ClientUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Nome e Sobrenome', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Celular', required=False)
    cpf = forms.CharField(label='CPF', required=False)
    birthday = forms.DateField(label='Aniversário', required=False)
    
    class Meta:
        model = User
        fields = ['email']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError('Por favor, informe seu nome completo.')
        return name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserClientAdressesForm(forms.ModelForm):
    class Meta:
        model = UserClientAdresses
        fields = ['zip_code', 'street', 'neighbor', 'number', 'city', 'state', 'complemento', 'reference_point']