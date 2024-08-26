from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Roles


@receiver(post_save, sender=User)
def create_default_user_profile(sender, instance, created, **kwargs):
    if created and check_roles():
        p = Profile(
            user=instance,
            role=Roles.objects.get(title="user")
        )
        p.save()


def check_roles():
    if Roles.objects.filter(title="user").count() > 0:
        return True
    return False
