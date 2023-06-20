# Generated by Django 4.1.7 on 2023-06-08 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("number", models.CharField(max_length=15)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("name", "user")},
            },
        ),
        migrations.CreateModel(
            name="Record",
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
                ("type", models.CharField(max_length=20, null=True)),
                ("time", models.TimeField(null=True)),
                ("dom", models.DateField(null=True)),
                ("booked", models.BooleanField(default=False)),
                ("acknowledged", models.BooleanField(default=False)),
                ("earnings", models.IntegerField()),
                (
                    "customer",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointments.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Acrylic Nails", "Acrylic Nails"),
                            ("Acrylic Toes", "Acrylic Toes"),
                            ("Nails and Toes", "Nails and Toes"),
                            ("Vacant", "Vacant"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("time", models.TimeField(null=True)),
                ("dom", models.DateField(null=True)),
                ("booked", models.BooleanField(default=False)),
                ("future", models.BooleanField(default=True)),
                (
                    "customer",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointments.customer",
                    ),
                ),
            ],
            options={
                "unique_together": {("time", "dom")},
            },
        ),
    ]