# Generated by Django 5.0.1 on 2024-08-26 12:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0002_alter_comments_options'),
        ('profiles', '0009_section_remove_profile_contest_profile_section'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_type',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='status',
            name='contest',
        ),
        migrations.AddField(
            model_name='application',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contest',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document_type',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project_type',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='profiles.section', verbose_name='Секция'),
            preserve_default=False,
        ),
    ]
