# Generated by Django 5.0.1 on 2024-09-23 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0031_alter_application_author_alter_application_contest_and_more'),
        ('locations', '0006_remove_locality_type_abbreviation_and_more'),
        ('meeting', '0003_meeting_status_section'),
        ('profiles', '0019_alter_section_logo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting_app',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='meeting_app',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='constructor.contest', verbose_name='Конкурс'),
        ),
        migrations.AlterField(
            model_name='meeting_app',
            name='locality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='locations.locality', verbose_name='Населенный пункт'),
        ),
        migrations.AlterField(
            model_name='meeting_app',
            name='municipal_district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='locations.municipal_district', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='meeting_app',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='profiles.section', verbose_name='Секция'),
        ),
        migrations.AlterField(
            model_name='meeting_app',
            name='settlement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='locations.settlement', verbose_name='Поселение'),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Наименование')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meeting_statuses', to='profiles.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.AlterField(
            model_name='meeting_app',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_set', to='meeting.status', verbose_name='Статус'),
        ),
        migrations.DeleteModel(
            name='Meeting_status',
        ),
    ]