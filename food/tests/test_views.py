from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from food.models import Dish, Restaurant


from food.models import Dish
from .data import *


class TestViewsHtml(TestCase):
    def test_signup_page(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/signup.html")

    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/login.html")

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/home.html")

    def test_cart_page(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/cart.html")

    def test_restaurants_page(self):
        response = self.client.get(reverse("restaurants"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/restaurants.html")

    def test_restaurant_page(self):
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

        id_ = Restaurant.objects.all().first().id
        response = self.client.get(reverse("restaurant", args=[id_]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/restaurant.html")

        dish = Dish.objects.create(
            name="dish",
            price=1.23,
            restaurant=restaurant,
            photo=picture,
        )
        dish.save()

        id_ = Dish.objects.all().first().id
        response = self.client.get(reverse("dish", args=[id_]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/dish.html")

        response = self.client.get(reverse("management"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/management.html")


class TestViewsFunctionality(TestCase):
    def test_signup_login_logout_user(self):
        response = self.client.post(reverse("signup"), SIGN_UP_DATA)
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse("login"), LOG_IN_DATA)
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse("logout"))
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse("management"), RESTAURANT_DATA)
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse("management"), RESTAURANT_DATA)
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse("address"), ORDER_DATA)
        self.assertEquals(response.status_code, 302)
