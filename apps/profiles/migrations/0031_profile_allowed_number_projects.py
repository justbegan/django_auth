# Generated by Django 5.0.1 on 2024-10-03 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0030_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='allowed_number_projects',
            field=models.PositiveIntegerField(default=0, verbose_name='Допустимое количество проектов'),
        ),
    ]
