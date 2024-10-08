# Generated by Django 5.0.1 on 2024-09-30 08:05

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0038_alter_custom_validation_code'),
        ('profiles', '0030_alter_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalContest',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Наименование')),
                ('grant_sum', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Сумма гранта')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('opened', 'Идет прием заявок'), ('tech_work', 'Идут подготовительные работы'), ('check', 'Идет проверка'), ('on_exam', 'Идет независимая экспертиза'), ('closed', 'Конкурс завершен')], default='new', max_length=120, verbose_name='Статус')),
                ('year', models.PositiveIntegerField(verbose_name='Год проведения')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='profiles.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'historical Конкурсы',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
