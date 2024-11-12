from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class ClientRegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Nome e Sobrenome', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Celular', required=False)
    cpf_cnpj = forms.CharField(label='CPF/CNPJ', required=False)
    birthday = forms.DateField(label='Aniversário', required=False)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
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
        