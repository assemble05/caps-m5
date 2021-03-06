# Generated by Django 4.0.6 on 2022-07-15 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0003_alter_service_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='id_provider',
        ),
        migrations.AddField(
            model_name='service',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='worked_services', to=settings.AUTH_USER_MODEL),
        ),
    ]
