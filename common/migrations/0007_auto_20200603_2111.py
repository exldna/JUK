# Generated by Django 3.0.5 on 2020-06-03 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='name',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='admin',
            name='surname',
            field=models.TextField(default=None),
        ),
    ]