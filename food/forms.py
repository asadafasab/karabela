"""Contains forms"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Dish
from .models import OpinionDish
from .models import OpinionRestaurant
from .models import Order
from .models import Restaurant


class LoginForm(forms.Form):
    """
    Login form for route /login
    Fields:
        username
        password
    """

    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "input is-primary mb-3",
                "type": "text",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "input is-primary mb-3",
                "type": "password",
                "placeholder": "Password",
            }
        ),
    )


class CreateUserForm(UserCreationForm):
    """
    Login form for route /signup
    Fields:
        username
        email
        password1
        password2
    """

    password1 = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "input is-primary mb-3",
                "type": "password",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "input is-primary mb-3",
                "type": "password",
                "placeholder": "Confirm password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "input is-primary mb-3",
                    "type": "text",
                    "placeholder": "Username",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "input is-primary mb-3",
                    "type": "email",
                    "placeholder": "Email",
                }
            ),
        }


class CreateRestaurant(ModelForm):
    """
    Login form for route /management
    Fields:
        name
        address
        description
        photo
        owner
    """

    class Meta:
        model = Restaurant
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input is-primary mb-3",
                    "type": "text",
                    "placeholder": "Restaurant's name",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "input is-primary mb-3",
                    "type": "text",
                    "placeholder": "Address",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea is-primary mb-3",
                    "type": "text",
                    "placeholder": "Description",
                }
            ),
            "photo": forms.FileInput(attrs={"class": "input is-primary mb-3"}),
        }


class CreateDish(ModelForm):
    """
    Login form for route /adddish
    Fields:
        name
        price
        description
        photo
        restaurant
    """

    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input is-primary mb-3",
                    "type": "text",
                    "placeholder": "Dish name",
                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "input is-primary mb-3",
                    "type": "text",
                    "placeholder": "price e.g. 12.01",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea is-primary mb-3",
                    "type": "text",
                    "placeholder": "Description",
                }
            ),
            "photo": forms.FileInput(attrs={"class": "input is-primary mb-3"}),
        }


class CreateRestaurantOpinion(ModelForm):
    """
    Login form for route /restaurant/<int:id>
    Fields:
        name
        price
        description
        photo
        restaurant
    """

    class Meta:
        model = OpinionRestaurant
        fields = "__all__"
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "textarea is-primary mb-3",
                    "type": "text",
                    "placeholder": "Review",
                }
            ),
            "recommendation": forms.CheckboxInput(
                attrs={"class": "checkbox", "type": "checkbox"}
            ),
        }


class CreateDishOpinion(ModelForm):
    """
    Login form for route /dish/<int:id>
    Fields:
        text (review)
        recommendation (score)
        dish
        user
    """

    class Meta:
        model = OpinionDish
        fields = "__all__"
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "textarea is-primary mb-3",
                    "type": "text",
                    "placeholder": "Review",
                }
            ),
            "recommendation": forms.TextInput(
                attrs={"class": "input", "type": "number"}
            ),
        }


class CreateOrder(ModelForm):
    """
    Login form for route /address
    Fields:
        text (review)
        recommendation (score)
        dish
        user
    """

    class Meta:
        model = Order
        fields = [
            "user",
            "region_address",
            "city_address",
            "street_address",
            "zip_code",
            "dishes",
        ]
        widgets = {
            "region_address": forms.TextInput(
                attrs={
                    "class": "input",
                    "type": "text",
                    "placeholder": "Region/State/Province",
                }
            ),
            "city_address": forms.TextInput(
                attrs={"class": "input", "type": "text", "placeholder": "City"}
            ),
            "street_address": forms.TextInput(
                attrs={
                    "class": "input",
                    "type": "text",
                    "placeholder": "Street and number of smth",
                }
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "input", "type": "text", "placeholder": "Zip code"}
            ),
        }
