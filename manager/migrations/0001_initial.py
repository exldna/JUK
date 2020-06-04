# Generated by Django 3.0.6 on 2020-05-30 16:32

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=200)),
                ('userEmail', models.EmailField(max_length=50)),
                ('ukEmail', models.EmailField(max_length=50)),
                ('date', models.CharField(max_length=50)),
                ('appointment', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=50)),
                ('finished', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publicationTag', models.CharField(choices=[('INTERESTING', 'interesting'), ('IMPORTANT', 'important'), ('URGENTLY', 'urgently')], default='INTERESTING', max_length=11)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('publicationDate', models.DateTimeField(verbose_name='date published')),
                ('publicationTitle', models.CharField(max_length=50)),
                ('publicationText', martor.models.MartorField()),
                ('donation_on', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.Company')),
            ],
        ),
    ]
