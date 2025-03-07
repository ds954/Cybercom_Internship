# Generated by Django 5.1.6 on 2025-02-14 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Userinfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=255)),
                ("lastname", models.CharField(max_length=255)),
                ("college_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
    ]
