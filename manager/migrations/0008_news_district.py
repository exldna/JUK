# Generated by Django 3.0.5 on 2020-05-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_news_publicationtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='district',
            field=models.CharField(max_length=140, null=True),
        ),
    ]
