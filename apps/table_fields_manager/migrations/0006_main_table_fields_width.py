# Generated by Django 5.0.1 on 2024-10-17 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_fields_manager', '0005_alter_main_table_fields_filter_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_table_fields',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина'),
        ),
    ]