# Generated by Django 3.0.3 on 2020-04-12 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0005_discussion_anon_allowed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='anon_allowed',
            field=models.TextField(default=0),
        ),
    ]
