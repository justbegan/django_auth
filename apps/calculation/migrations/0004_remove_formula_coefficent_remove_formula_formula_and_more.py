# Generated by Django 5.0.1 on 2024-08-30 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0003_alter_formula_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formula',
            name='coefficent',
        ),
        migrations.RemoveField(
            model_name='formula',
            name='formula',
        ),
        migrations.RemoveField(
            model_name='formula',
            name='hight_value',
        ),
        migrations.RemoveField(
            model_name='formula',
            name='scope',
        ),
        migrations.AddField(
            model_name='formula',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]