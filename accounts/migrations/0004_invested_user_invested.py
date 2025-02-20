# Generated by Django 5.1.3 on 2024-12-08 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email'),
        ('stocks', '0003_stock_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invested',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveBigIntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='invested',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.invested'),
        ),
    ]
