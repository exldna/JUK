# Generated by Django 3.0.3 on 2020-04-18 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0014_auto_20200418_1311'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='HelpDeskSmartMessage',
        ),
    ]