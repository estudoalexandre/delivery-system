from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

# Create your models here.



class Store(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    
    # Campos detalhados para o endereço
    street = models.CharField("Rua", max_length=255)
    number = models.CharField("Número", max_length=20)
    neighborhood = models.CharField("Bairro", max_length=100)
    city = models.CharField("Cidade", max_length=100)
    state = models.CharField("Estado", max_length=2)  
    postal_code = models.CharField("CEP", max_length=9)  
    
    phone = models.CharField(max_length=20)
    open_time = models.CharField(max_length=20)
    close_time = models.CharField(max_length=20)
    image = models.ImageField(upload_to='stores/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def full_address(self):
        return f"{self.street}, {self.number}, {self.neighborhood}, {self.city} - {self.state}, {self.postal_code}"

    def save(self, *args, **kwargs):
        # Verifica se o owner está no grupo "Lojista"
        if self.owner:
            lojista_group = Group.objects.get(name='Lojista')
            if not self.owner.groups.filter(id=lojista_group.id).exists():
                raise ValidationError("O usuário selecionado deve fazer parte do grupo Lojista.")
        super().save(*args, **kwargs)
        
class Categoria(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(Categoria, related_name='products' ,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.name