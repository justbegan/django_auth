# Generated by Django 5.0.1 on 2024-09-30 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0037_alter_custom_validation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_validation',
            name='code',
            field=models.TextField(default='#python!\n# imported models Application, Profile\ncurrent_user = request.user\ncurrent_contest = get_current_contest(request)\nprofile_type = Profile.objects.get(user__id=current_user.id).profile_type\n', verbose_name='Код'),
        ),
    ]
