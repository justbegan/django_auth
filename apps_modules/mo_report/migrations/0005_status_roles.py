# Generated by Django 5.0.1 on 2024-11-06 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mo_report', '0004_remove_mo_report_app_status'),
        ('profiles', '0036_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='roles',
            field=models.ManyToManyField(related_name='%(app_label)s_set', to='profiles.roles'),
        ),
    ]
