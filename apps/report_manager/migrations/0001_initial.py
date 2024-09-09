# Generated by Django 5.0.1 on 2024-08-29 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0010_section_header_section_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Наименование')),
                ('url', models.URLField(verbose_name='Ссылка на отчет')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': 'Отчеты',
            },
        ),
    ]