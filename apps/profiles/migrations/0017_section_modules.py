# Generated by Django 5.0.1 on 2024-09-19 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_manager', '0001_initial'),
        ('profiles', '0016_roles_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='modules',
            field=models.ManyToManyField(blank=True, to='module_manager.apps', verbose_name='Модули'),
        ),
    ]