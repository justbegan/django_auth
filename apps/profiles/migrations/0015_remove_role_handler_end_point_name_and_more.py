# Generated by Django 5.0.1 on 2024-09-09 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0014_rename_role_role_handler_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role_handler',
            name='end_point_name',
        ),
        migrations.AddField(
            model_name='role_handler',
            name='model',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype', verbose_name='Модель'),
            preserve_default=False,
        ),
    ]
