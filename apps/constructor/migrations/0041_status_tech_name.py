# Generated by Django 5.0.1 on 2024-10-15 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0040_alter_application_project_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='tech_name',
            field=models.CharField(default=1, max_length=30, verbose_name='Тех. название'),
            preserve_default=False,
        ),
    ]