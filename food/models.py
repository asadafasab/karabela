import json

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=300)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    description = models.CharField(max_length=400)
    photo = models.ImageField(upload_to="bg")

    def __str__(self):
        return f"{self.name}, {self.owner}, {self.address}"


class Dish(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    description = models.CharField(max_length=512)
    photo = models.ImageField(upload_to="dish")

    def __str__(self):
        return f"{self.name}, {self.price}"


class OpinionRestaurant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    recommendation = models.BooleanField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text},\n{self.recommendation}"


class OpinionDish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text},\n{self.score}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    # status of the order
    # default/not payed (0, None),payed(1), doing (2), complete (3)
    status = models.PositiveIntegerField(validators=[MaxValueValidator(3)], null=True)
    dishes = models.JSONField()
    region_address = models.CharField(max_length=128)
    city_address = models.CharField(max_length=128)
    street_address = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.dishes}, {self.status}"
