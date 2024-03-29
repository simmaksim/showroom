# Generated by Django 4.1.4 on 2023-01-30 20:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "year",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1940),
                            django.core.validators.MaxValueValidator(2024),
                        ]
                    ),
                ),
                ("brand", models.CharField(max_length=50)),
                ("model", models.CharField(max_length=50)),
                ("image", models.URLField()),
                ("vin", models.CharField(max_length=17)),
                (
                    "power",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("WH", "White"),
                            ("RE", "Red"),
                            ("GR", "Green"),
                            ("BL", "Blue"),
                            ("BK", "Black"),
                        ],
                        default="BK",
                        max_length=20,
                    ),
                ),
                (
                    "body",
                    models.CharField(
                        choices=[
                            ("SE", "Sedan"),
                            ("HB", "Hatchback"),
                            ("LB", "Liftback"),
                            ("CO", "Crossover"),
                            ("UN", "Universal"),
                            ("PU", "Pickup"),
                            ("MV", "Minivan"),
                        ],
                        default="SE",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Client",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=50)),
                ("surname", models.CharField(max_length=50)),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("location", django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Provider",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=50)),
                ("clients_count", models.IntegerField(default=0)),
                ("location", django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Showroom",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=50)),
                ("location", django_countries.fields.CountryField(max_length=2)),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "criteries",
                    models.JSONField(
                        blank=True,
                        default={
                            "body": "",
                            "brand": "",
                            "color": "",
                            "model": "",
                            "power": 0,
                            "year": "",
                        },
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShowroomSales",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "sale",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="showroom_sales_car",
                        to="showroom.car",
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="showrooms_sales_showroom",
                        to="showroom.showroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShowroomCar",
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
                    "cars_count",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="showroom_car_cars",
                        to="showroom.car",
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="showroom_car_showrooms",
                        to="showroom.showroom",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="showroom",
            name="cars",
            field=models.ManyToManyField(
                through="showroom.ShowroomCar", to="showroom.car"
            ),
        ),
        migrations.AddField(
            model_name="showroom",
            name="unique_clients",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="unique_clients",
                to="showroom.client",
            ),
        ),
        migrations.CreateModel(
            name="SaleHistory",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_history_cars",
                        to="showroom.car",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_history_clients",
                        to="showroom.client",
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_history_showrooms",
                        to="showroom.showroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProviderSales",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "sale",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="provider_sales_cars",
                        to="showroom.car",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="providers_sales_provider",
                        to="showroom.provider",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProviderCar",
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
                    "cars_count",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="provider_car_cars",
                        to="showroom.car",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="provider_car_providers",
                        to="showroom.provider",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="provider",
            name="cars",
            field=models.ManyToManyField(
                through="showroom.ProviderCar", to="showroom.car"
            ),
        ),
    ]
