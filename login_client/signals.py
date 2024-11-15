from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserClientProfile
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='Cliente').exists():
        UserClientProfile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    if instance.groups.filter(name='Cliente').exists():
        instance.userclientprofile.save()