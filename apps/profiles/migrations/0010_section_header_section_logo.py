# Generated by Django 5.0.1 on 2024-08-27 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_section_remove_profile_contest_profile_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='header',
            field=models.TextField(blank=True, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='section',
            name='logo',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на лого'),
        ),
    ]
