# Generated by Django 5.1.3 on 2024-11-20 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_domesticstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='color',
            field=models.CharField(choices=[('#A6F7E2', '삼성전자'), ('#B79BFF', 'SK하이닉스'), ('#FFE5A5', 'LG에너지솔루션'), ('#C7FFA5', '삼성바이오로직스'), ('#F8A5FF', '현대차')], default='#A6F7E2', max_length=50),
        ),
    ]
