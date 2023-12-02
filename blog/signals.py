from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        # user_profile.follow.add(instance.profile)
        # user_profile.save()

