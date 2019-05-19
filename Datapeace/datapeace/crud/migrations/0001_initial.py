# Generated by Django 2.1.7 on 2019-05-18 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('web', models.URLField(max_length=100)),
                ('age', models.IntegerField(default=0)),
            ],
        ),
    ]