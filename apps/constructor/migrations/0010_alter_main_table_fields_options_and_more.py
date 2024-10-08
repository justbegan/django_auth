# Generated by Django 5.0.1 on 2024-08-28 02:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0009_main_table_fields'),
        ('profiles', '0010_section_header_section_logo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='main_table_fields',
            options={'verbose_name': 'Отображаемые значения в главной таблице'},
        ),
        migrations.AddField(
            model_name='main_table_fields',
            name='field',
            field=models.CharField(default=1, verbose_name='Транскрипция'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='main_table_fields',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
    ]
