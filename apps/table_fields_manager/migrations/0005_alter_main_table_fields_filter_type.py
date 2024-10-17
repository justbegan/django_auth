# Generated by Django 5.0.1 on 2024-10-17 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_fields_manager', '0004_alter_main_table_fields_filter_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_table_fields',
            name='filter_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Справочник'), (2, 'Кастомный'), (3, 'Булево')], null=True, verbose_name='Тип'),
        ),
    ]