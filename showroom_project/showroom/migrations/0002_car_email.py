# Generated by Django 4.1.4 on 2023-01-10 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showroom", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="email",
            field=models.CharField(default="", max_length=10),
        ),
    ]