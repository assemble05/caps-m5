# Generated by Django 4.0.6 on 2022-07-14 13:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=35)),
                ('city', models.CharField(max_length=35)),
                ('street', models.CharField(max_length=105)),
                ('number', models.PositiveIntegerField()),
                ('complementet', models.CharField(max_length=255, null=True)),
                ('zip_code', models.CharField(max_length=15)),
            ],
        ),
    ]
