# Generated by Django 5.0.1 on 2024-09-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone_book', '0002_phone_book_created_at_phone_book_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone_book',
            name='ip_phone',
            field=models.CharField(default=1, max_length=20, verbose_name='Телефон'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phone_book',
            name='position',
            field=models.TextField(verbose_name='Должность'),
        ),
    ]
