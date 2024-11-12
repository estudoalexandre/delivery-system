from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=100)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            try:
                # Tenta buscar o usuário pelo email e autenticar com a senha
                user = User.objects.get(email=email)
                self.user_cache = authenticate(self.request, username=user.username, password=password)
            except User.DoesNotExist:
                self.user_cache = None

            if self.user_cache is None:
                raise self.get_invalid_login_error()
        return self.cleaned_data

class LojistaRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()
        
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='Lojista'))
        return user