from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Roles


@receiver(post_save, sender=User)
def create_default_user_profile(sender, instance, created, **kwargs):
    if created:
        p = Profile(
            user=instance,
            role=Roles.objects.first()
        )
        p.save()
