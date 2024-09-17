from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import (Locality, Settlement)


@receiver(post_save, sender=Locality)
def locality_post_save(sender, instance, created, **kwargs):
    cache.delete("all_locality")


@receiver(post_delete, sender=Locality)
def locality_post_delete(sender, instance, **kwargs):
    cache.delete("all_locality")


@receiver(post_save, sender=Settlement)
def settlement_post_save(sender, instance, created, **kwargs):
    cache.delete("all_settlements")


@receiver(post_delete, sender=Settlement)
def settlement_post_delete(sender, instance, **kwargs):
    cache.delete("all_settlements")
