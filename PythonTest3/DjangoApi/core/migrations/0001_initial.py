# Generated by Django 5.1.6 on 2025-03-31 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
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
                ("department_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=100)),
                ("firstname", models.CharField(max_length=100)),
                ("lastname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
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
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("joined_date", models.DateField(auto_now_add=True)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmployeeProfile",
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
                ("profile_picture", models.ImageField(upload_to="")),
                (
                    "Employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.employee"
                    ),
                ),
            ],
        ),
    ]
