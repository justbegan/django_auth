# Generated by Django 5.0.1 on 2024-12-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0038_alter_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='amount_of_subsidy',
            field=models.CharField(default=123, max_length=500, verbose_name='Объем субсидий'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='goal',
            field=models.CharField(default=123, max_length=500, verbose_name='Цель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='key_terms',
            field=models.CharField(default=123, max_length=2000, verbose_name='Ключевые условия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='members',
            field=models.CharField(default=123, max_length=500, verbose_name='Участники'),
            preserve_default=False,
        ),
    ]
