# Generated by Django 5.0.1 on 2024-12-02 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0053_calculated_fields_func_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculated_fields',
            name='contest',
            field=models.ManyToManyField(blank=True, to='constructor.contest', verbose_name='Конкурс'),
        ),
    ]
