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

