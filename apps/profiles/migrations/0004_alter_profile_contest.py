# Generated by Django 5.0.1 on 2024-02-29 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contest',
            field=models.CharField(choices=[('65a766112e0fe1554e0d3c99', 'Тестовый конкурс'), ('65a767c72e0fe1554e0d3c9a', 'Конкурс для СМИ')], max_length=120, verbose_name='Конкурс'),
        ),
    ]