from django import forms
from django.contrib.auth.models import User, Group
from .models import Store, Categoria, Product

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
        'name',
        'slug',
        'description',
        'street',
        'number',
        'neighborhood',
        'city',
        'state',
        'postal_code',
        'phone',
        'open_time',
        'close_time',
        'image'
    ]


class CategoryProductForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'description',
            'image',
            # 'categoria'
        ]
        widgets = {
            'categoria': forms.Select(attrs={'required': False}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)