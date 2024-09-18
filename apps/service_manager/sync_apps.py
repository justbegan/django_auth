from django.core.management.base import BaseCommand
from apps.service_manager.models import Apps
from django.apps import apps


class Command(BaseCommand):
    help = 'Синхронизация приложений с базой данных'

    def handle(self, *args, **kwargs):
        apps_list = apps.get_app_configs()
        for app in apps_list:
            # Проверяем, существует ли приложение, если нет - создаем
            Apps.objects.get_or_create(
                name=app.name,
                defaults={'verbose_name': app.verbose_name}
            )
        self.stdout.write(self.style.SUCCESS('Приложения синхронизированы с базой данных.'))
