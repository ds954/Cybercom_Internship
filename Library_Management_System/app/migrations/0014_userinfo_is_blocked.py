# Generated by Django 5.1.6 on 2025-04-14 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_userinfo_login_time_userinfo_logout_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="is_blocked",
            field=models.BooleanField(default=False),
        ),
    ]
