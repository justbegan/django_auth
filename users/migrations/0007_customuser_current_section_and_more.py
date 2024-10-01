# Generated by Django 5.0.1 on 2024-10-01 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0030_alter_profile_user'),
        ('users', '0006_historicalcustomuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='current_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.section', verbose_name='Текущая секция'),
        ),
        migrations.AddField(
            model_name='historicalcustomuser',
            name='current_section',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='profiles.section', verbose_name='Текущая секция'),
        ),
    ]