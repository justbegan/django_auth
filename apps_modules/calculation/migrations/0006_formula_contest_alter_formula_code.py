# Generated by Django 5.0.1 on 2024-11-19 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0005_remove_formula_field'),
        ('constructor', '0048_alter_schema_contests'),
    ]

    operations = [
        migrations.AddField(
            model_name='formula',
            name='contest',
            field=models.ManyToManyField(blank=True, to='constructor.contest', verbose_name='Конкурс'),
        ),
        migrations.AlterField(
            model_name='formula',
            name='code',
            field=models.TextField(default='#python!\n# result - пустой dict\n# key - названия поля\n# value - значение поля\nresult[key] =\n', verbose_name='Код'),
        ),
    ]
