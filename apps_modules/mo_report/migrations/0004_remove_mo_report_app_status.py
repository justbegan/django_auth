# Generated by Django 5.0.1 on 2024-11-02 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mo_report', '0003_alter_mo_report_app_locality_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mo_report_app',
            name='status',
        ),
    ]