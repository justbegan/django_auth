# Generated by Django 5.0.1 on 2024-11-26 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0048_alter_schema_contests'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculated_fields',
            name='field_type',
            field=models.IntegerField(choices=[(1, 'IntegerField'), (2, 'CharField'), (3, 'FloatField'), (4, 'DecimalField')], default=2, verbose_name='Тип поля'),
        ),
    ]
