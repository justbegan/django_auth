# Generated by Django 5.0.1 on 2024-10-16 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0006_status_tech_name_alter_status_section'),
        ('profiles', '0034_alter_profile_type_abbreviation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_set', to='profiles.section', verbose_name='Секция'),
        ),
    ]
