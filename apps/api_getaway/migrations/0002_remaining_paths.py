# Generated by Django 5.0.1 on 2024-02-09 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_getaway', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remaining_paths',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.roles', verbose_name='Роль')),
            ],
            options={
                'verbose_name': 'Приватный путь',
                'verbose_name_plural': 'Приватные пути',
            },
        ),
    ]
