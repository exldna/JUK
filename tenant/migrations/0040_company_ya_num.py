# Generated by Django 3.0.5 on 2020-05-25 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tenant', '0039_auto_20200524_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ya_num',
            field=models.IntegerField(default=None),
        ),
    ]
