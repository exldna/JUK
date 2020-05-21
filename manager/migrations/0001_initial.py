
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=50)),
                ('publicationDate', models.DateTimeField(verbose_name='date published')),
                ('publicationTitle', models.CharField(max_length=50)),
                ('publicationText', models.TextField(max_length=5000)),
            ],
        ),
    ]
