from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

from .models import (Locality, Settlement)


logger = logging.getLogger('django')


@receiver(post_save, sender=Locality)
def locality_post_save(sender, instance, created, **kwargs):
    try:
        cache.delete("all_locality")
    except Exception as e:
        logger.exception(f"redis не найден {e}")


@receiver(post_delete, sender=Locality)
def locality_post_delete(sender, instance, **kwargs):
    try:
        cache.delete("all_locality")
    except Exception as e:
        logger.exception(f"redis не найден {e}")


@receiver(post_save, sender=Settlement)
def settlement_post_save(sender, instance, created, **kwargs):
    try:
        cache.delete("all_settlements")
    except Exception as e:
        logger.exception(f"redis не найден {e}")


@receiver(post_delete, sender=Settlement)
def settlement_post_delete(sender, instance, **kwargs):
    try:
        cache.delete("all_settlements")
    except Exception as e:
        logger.exception(f"redis не найден {e}")
