# Generated by Django 5.1.6 on 2025-04-15 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="username",
            field=models.CharField(max_length=100),
        ),
    ]
