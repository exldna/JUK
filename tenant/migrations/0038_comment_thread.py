# Generated by Django 3.0.5 on 2020-05-24 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0037_auto_20200522_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Comment'),
        ),
    ]