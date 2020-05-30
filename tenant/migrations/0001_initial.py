# Generated by Django 3.0.6 on 2020-05-30 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.TextField()),
                ('cr_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.IntegerField()),
                ('name', models.TextField()),
                ('ya_num', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, default='static/default.jpg', upload_to='photo')),
                ('flat', models.TextField()),
                ('is_vol', models.BooleanField(default=False)),
                ('test_date', models.DateTimeField(default=None, null=True)),
                ('house_confirmed', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.House')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=20)),
                ('task', models.TextField(max_length=100)),
                ('cr_date', models.DateTimeField(auto_now=True)),
                ('status', models.TextField(max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('volunteer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cr_date', models.DateTimeField()),
                ('status', models.TextField()),
                ('target', models.TextField()),
                ('name', models.TextField(blank=True, null=True)),
                ('surname', models.TextField(blank=True, null=True)),
                ('patronymic', models.TextField(blank=True, null=True)),
                ('model', models.TextField(blank=True, null=True)),
                ('color', models.TextField(blank=True, null=True)),
                ('number', models.TextField(blank=True, null=True)),
                ('aim', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='Antosha')),
                ('surname', models.TextField(default='Andreev')),
                ('status', models.IntegerField(choices=[(1, 'Accepted'), (2, 'Refused'), (3, 'Not considered')], default=3)),
                ('inn_company', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, default='static/default.jpg', upload_to='photo')),
                ('is_admin', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(default='Вода|Электричество|Другое', max_length=100)),
                ('company', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Company')),
                ('house', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.House')),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.TextField()),
                ('category', models.TextField()),
                ('description', models.TextField()),
                ('cr_date', models.DateTimeField()),
                ('anon_allowed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.Forum')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', martor.models.MartorField()),
                ('cr_date', models.DateTimeField()),
                ('anon', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('discussion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Discussion')),
                ('thread', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='AppealMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', martor.models.MartorField()),
                ('cr_date', models.DateTimeField()),
                ('appeal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.Appeal')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appeal',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Manager'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Tenant'),
        ),
    ]
