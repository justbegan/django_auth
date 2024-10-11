# Generated by Django 5.0.1 on 2024-10-10 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('table_fields_manager', '0002_main_table_fields_filter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_table_fields',
            name='filter_config',
            field=models.JSONField(blank=True, null=True, verbose_name='Настройки поля'),
        ),
        migrations.AlterField(
            model_name='main_table_fields',
            name='filter',
            field=models.BooleanField(default=False, verbose_name='Фильтруемый'),
        ),
        migrations.AlterField(
            model_name='main_table_fields',
            name='filter_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='table_fields_manager_filter_type', to='contenttypes.contenttype', verbose_name='Класс справочника'),
        ),
    ]