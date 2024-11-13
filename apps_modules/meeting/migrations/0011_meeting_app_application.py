# Generated by Django 5.0.1 on 2024-11-13 02:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0046_alter_status_roles_calculated_fields'),
        ('meeting', '0010_alter_status_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting_app',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='constructor.application', verbose_name='Заявка'),
        ),
    ]
