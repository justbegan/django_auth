# Generated by Django 5.0.1 on 2024-12-05 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_locality_sections'),
        ('profiles', '0040_section_adt'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contest_type',
            field=models.ForeignKey(default=1, help_text='Для какого конкурса этот профиль будет участвовать', on_delete=django.db.models.deletion.PROTECT, to='locations.district_type', verbose_name='Тип конкурса'),
            preserve_default=False,
        ),
    ]