# Generated by Django 4.0.6 on 2022-07-15 16:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_initial"),
        ("reviews", "0003_alter_review_stars"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="service",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="services.service",
            ),
            preserve_default=False,
        ),
    ]
