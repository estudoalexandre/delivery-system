from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserClientAdresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    neighbor = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    reference_point = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.street