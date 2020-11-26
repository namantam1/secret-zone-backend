from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile, Friends

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Friends.objects.create(user=instance)

@receiver(post_save, sender=Friends)
def friends_signal(sender, instance, created, **kwargs):
    print(sender, instance, created, kwargs)