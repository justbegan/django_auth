# Generated by Django 5.0.1 on 2024-10-28 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0043_alter_application_locality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document_type',
            name='title',
            field=models.TextField(verbose_name='Наименование'),
        ),
    ]
