# Generated by Django 5.0.1 on 2024-11-15 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0046_alter_status_roles_calculated_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='contests',
            field=models.ManyToManyField(to='constructor.contest', verbose_name='Конкурсы'),
        ),
    ]
