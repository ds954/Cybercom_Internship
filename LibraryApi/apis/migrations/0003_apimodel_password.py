# Generated by Django 5.1.6 on 2025-02-24 11:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0002_apimodel_email_apimodel_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="apimodel",
            name="password",
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
