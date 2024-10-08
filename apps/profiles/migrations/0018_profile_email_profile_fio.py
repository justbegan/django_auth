# Generated by Django 5.0.1 on 2024-09-20 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_section_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='profile',
            name='fio',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ФИО'),
        ),
    ]
