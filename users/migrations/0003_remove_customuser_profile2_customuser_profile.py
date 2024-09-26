# Generated by Django 5.0.1 on 2024-09-25 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0027_remove_profile_user'),
        ('users', '0002_customuser_profile2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profile2',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]
