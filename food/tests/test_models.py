from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .data import *

from food.models import Dish, Restaurant


class TestModels(TestCase):
    def test_bunch_of_things(self):
        response = self.client.post(reverse("signup"), SIGN_UP_DATA)
        user = User.objects.all().first()

        response = self.client.post(reverse("login"), LOG_IN_DATA)
        picture = SimpleUploadedFile("gif.gif", GIF, content_type="image/gif")
        restaurant = Restaurant.objects.create(
            name="restaurant",
            owner=user,
            address="Address",
            description="description",
            photo=picture,
        )
        restaurant.save()

        self.assertEqual(restaurant.name, "restaurant")

        dish = Dish.objects.create(
            name="dish",
            price=1.23,
            restaurant=restaurant,
            photo=picture,
        )
        dish.save()

        self.assertEqual(dish.name, "dish")
