# Generated by Django 5.0.1 on 2024-08-26 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contest',
            field=models.CharField(blank=True, choices=[('65a766112e0fe1554e0d3c99', 'Тестовый конкурс'), ('65a767c72e0fe1554e0d3c9a', 'Конкурс для СМИ'), ('65e57e978c1d50bee38f284e', 'Тестовый конкурс 123')], max_length=120, null=True, verbose_name='Конкурс'),
        ),
    ]