# Generated by Django 5.1.3 on 2024-12-08 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_invested_user_invested'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invested',
            old_name='total',
            new_name='input',
        ),
        migrations.RemoveField(
            model_name='user',
            name='invested',
        ),
        migrations.AddField(
            model_name='invested',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
