# Generated by Django 3.0.5 on 2020-05-07 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='photo',
            field=models.ImageField(blank=True, default='static/default.jpg', upload_to='photo'),
        ),
    ]