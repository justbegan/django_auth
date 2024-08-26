# Generated by Django 5.0.1 on 2024-08-26 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0002_alter_comments_options'),
        ('profiles', '0007_remove_profile_contest_profile_locality_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='constructor.contest', verbose_name='Конкурс'),
        ),
    ]
