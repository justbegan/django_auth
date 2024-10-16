# Generated by Django 5.0.1 on 2024-10-16 00:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0005_alter_meeting_app_author'),
        ('profiles', '0034_alter_profile_type_abbreviation'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='tech_name',
            field=models.CharField(default=1, max_length=30, verbose_name='Тех. название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='status',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='profiles.section', verbose_name='Секция'),
        ),
    ]
