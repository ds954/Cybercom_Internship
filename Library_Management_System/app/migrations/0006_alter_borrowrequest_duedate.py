# Generated by Django 5.1.6 on 2025-03-12 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_alter_borrowrequest_duedate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowrequest",
            name="Duedate",
            field=models.DateField(default=datetime.date(2025, 5, 11)),
        ),
    ]
