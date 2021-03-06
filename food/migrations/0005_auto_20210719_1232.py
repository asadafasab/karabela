# Generated by Django 3.2.5 on 2021-07-19 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0004_auto_20210719_1137"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="background",
            field=models.ImageField(upload_to="bg"),
        ),
        migrations.CreateModel(
            name="Dish",
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
                ("name", models.CharField(max_length=300)),
                ("price", models.DecimalField(decimal_places=2, max_digits=4)),
                ("photo", models.ImageField(upload_to="dish")),
                ("description", models.CharField(max_length=512)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="food.restaurant",
                    ),
                ),
            ],
        ),
    ]
