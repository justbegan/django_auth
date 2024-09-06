# Generated by Django 5.0.1 on 2024-09-06 03:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('constructor', '0024_delete_comments'),
        ('locations', '0006_remove_locality_type_abbreviation_and_more'),
        ('profiles', '0014_rename_role_role_handler_roles'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='Meeting_schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Наименование')),
                ('properties', models.JSONField(default=dict, verbose_name='Properties')),
                ('required', models.JSONField(blank=True, default=list, null=True, verbose_name='Required')),
                ('type', models.CharField(max_length=120, verbose_name='Тип')),
                ('section', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'Схема',
                'verbose_name_plural': 'Схемы',
            },
        ),
        migrations.CreateModel(
            name='Meeting_app',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания обращения')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('custom_data', models.JSONField(default=dict, verbose_name='Кастомные поля')),
                ('documents', models.JSONField(default=list, verbose_name='Документы')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='constructor.contest', verbose_name='Статус')),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.locality', verbose_name='Населенный пункт')),
                ('municipal_district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.municipal_district', verbose_name='Район')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция')),
                ('settlement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.settlement', verbose_name='Поселение')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='meeting.meeting_status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Собрание',
                'verbose_name_plural': 'Собрания',
            },
        ),
    ]
