# Generated by Django 3.0.3 on 2020-04-12 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0006_auto_20200412_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tenant.Comment'),
        ),
    ]