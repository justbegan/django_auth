# Generated by Django 5.0.1 on 2024-08-28 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0010_section_header_section_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Название')),
                ('field', models.CharField(max_length=120, verbose_name='Поле')),
                ('formula', models.CharField(max_length=120, verbose_name='Формула')),
                ('scope', models.FloatField(default=0, verbose_name='Сравниваемое значение')),
                ('hight_value', models.FloatField(default=0, verbose_name='Получаемый бал если соответует критерию')),
                ('coefficent', models.FloatField(default=0, verbose_name='Коефицент')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'Формула',
                'verbose_name_plural': 'Формулы',
            },
        ),
    ]
