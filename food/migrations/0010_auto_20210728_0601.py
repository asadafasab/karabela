# Generated by Django 3.2.5 on 2021-07-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0009_alter_order_dishes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="total_price",
        ),
        migrations.AlterField(
            model_name="order",
            name="dishes",
            field=models.JSONField(),
        ),
    ]
