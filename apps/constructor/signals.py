from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application
from apps_modules.mo_report.models import Mo_report_app, Status


@receiver(post_save, sender=Application)
def create_default_user_profile(sender, instance, created, **kwargs):
    conditions = [
        instance.section.modules.filter(name='apps_modules.mo_report').exists(),
        instance.status.tech_name == 'presented',
        not created
    ]
    if all(conditions):
        mo_report = Mo_report_app.objects.create(
            municipal_district=instance.municipal_district,
            settlement=instance.settlement,
            locality=instance.locality,
            status=Status.objects.get(tech_name='presented', section=instance.section),
            contest=instance.contest,
            author=instance.author,
            section=instance.section,
            application=instance
        )
        mo_report.save()
