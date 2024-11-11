# Generated by Django 5.0.1 on 2024-11-11 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mo_report', '0005_status_roles'),
        ('profiles', '0036_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='%(app_label)s_set', to='profiles.roles'),
        ),
    ]
