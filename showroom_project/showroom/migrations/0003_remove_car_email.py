# Generated by Django 4.1.4 on 2023-01-10 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("showroom", "0002_car_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="car",
            name="email",
        ),
    ]
