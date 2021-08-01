"""Contains view functions"""

import json

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse

from .models import Restaurant, Dish, OpinionDish, OpinionRestaurant, Order
from .forms import (
    CreateUserForm,
    LoginForm,
    CreateDish,
    CreateOrder,
    CreateDishOpinion,
    CreateRestaurant,
    CreateRestaurantOpinion,
)


def home(request):
    """Home page. Roure for '' and 'home'."""
    dishes = Dish.objects.all()[:10]
    restaurants = Restaurant.objects.all()[:10]

    context = {"dishes": dishes, "restaurants": restaurants}
    return render(request, "food/home.html", context)


def sign_up(request):
    """
    Sign up page. Roure for 'signup'.
    Creates new user (or smth).
    """

    if request.user.is_authenticated:
        return redirect("/")
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Accout was created for {username}")
            return redirect("login")
    return render(request, "food/signup.html", {"form": form})


def log_in(request):
    """Log in page. Roure for 'login'."""

    if request.user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Something's wrong, I can feel it")

    return render(request, "food/login.html", {"form": form})


@login_required(login_url="login")
def log_out(request):
    """Log out page. Roure for 'logout'."""
    logout(request)
    messages.info(request, "Logged out")
    return redirect("login")


def cart(request):
    """Cart page. Roure for 'cart'."""
    return render(request, "food/cart.html", {})


def restaurants(request):
    """
    Page with all restaurants (from db).
    Roure for 'restaurants'.
    """

    query = Restaurant.objects.all()
    context = {"restaurants": query}
    return render(request, "food/restaurants.html", context)


def restaurant(request, id):
    """
    Page of a specific restaurant.
    Can create new review of a restaurant
    Roure for 'restaurant/<int:id>'.
    """
    restaurant_ = Restaurant.objects.get(id=id)
    dishes = Dish.objects.filter(restaurant=id)
    reviews = OpinionRestaurant.objects.filter(restaurant=restaurant_)
    positive_reviews = OpinionRestaurant.objects.filter(
        restaurant=restaurant_, recommendation=True
    ).count()
    review_count = reviews.count()
    if review_count and positive_reviews:
        ratio = round(positive_reviews / review_count, 2) * 100
    else:
        ratio = 0.0

    if request.method == "POST":
        form = CreateRestaurantOpinion(request.POST, instance=review)
        if form.is_valid():
            form.save()
            id_ = request.POST["restaurant"]
            messages.info(request, "Added your review")
            return redirect(f"/restaurant/{id_}")

    context = {
        "info": restaurant_,
        "dishes": dishes,
        "ratio": ratio,
        "reviews": reviews,
        "reviewCount": review_count,
    }

    if request.user.is_authenticated:
        review = OpinionRestaurant.objects.filter(
            user=request.user, restaurant=restaurant_
        ).first()

        fill = {
            "user": request.user,
            "restaurant": restaurant_,
        }
        if review:
            fill["text"] = review.text
            fill["recomendation"] = review.recommendation

            form_edit_review = CreateRestaurantOpinion(fill)
        else:
            form_edit_review = CreateRestaurantOpinion(fill)
        context["formEditReview"] = form_edit_review

    if request.user == restaurant_.owner:
        form_dish = CreateDish({"restaurant": restaurant_})
        context["formDish"] = form_dish

    return render(request, "food/restaurant.html", context)


def dish(request, id):
    """
    Page of a specific dish.
    Can create new review of a dish
    Roure for 'dish/<int:id>'.
    """
    dish_ = Dish.objects.get(id=id)
    reviews_dish = OpinionDish.objects.filter(dish=id)
    score_avg = reviews_dish.aggregate(Avg("score"))["score__avg"]
    if score_avg:
        score_avg = round(score_avg, 1)

    context = {
        "dish": dish_,
        "reviews": reviews_dish,
        "avg": score_avg,
    }

    if request.user.is_authenticated:
        review = OpinionDish.objects.filter(user=request.user, dish=dish_).first()
        fill = {"user": request.user, "dish": dish_}
        if review:
            fill["text"] = review.text
            fill["score"] = review.score
        form = CreateDishOpinion(fill)
        context["form"] = form

        if request.method == "POST":
            form = CreateDishOpinion(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect(f"/dish/{id}")

    if dish_.restaurant.owner == request.user:
        form_dish = CreateDish(
            {
                "name": dish_.name,
                "price": dish_.price,
                "restaurant": dish_.restaurant,
                "description": dish_.description,
                "photo": dish_.photo,
            }
        )
        context["formDish"] = form_dish

    return render(request, "food/dish.html", context)


@login_required(login_url="login")
def management(request):
    """
    Page for restaurant management.
    Can create new restaurant.
    Roure for 'management'.
    """
    if request.method == "POST":
        form = CreateRestaurant(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management")

    query = Restaurant.objects.filter(owner=request.user.id)
    form_restaurant = CreateRestaurant({"owner": request.user})
    form_dish = CreateDish()
    orders = Order.objects.filter(user=request.user)

    context = {
        "restaurants": query,
        "formRestaurant": form_restaurant,
        "formDish": form_dish,
    }
    if orders:
        orders_obj = get_orders(orders)

        context["orders"] = orders_obj
    return render(request, "food/management.html", context)


@login_required(login_url="login")
def add_dish(request):
    """Add dish. Roure for 'adddish'."""
    if request.method == "POST":
        form = CreateDish(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Added new dish.")
        messages.info(request, "Something went wrong.")

    id_ = request.POST["restaurant"]
    return redirect(f"/restaurant/{id_}")


@login_required(login_url="login")
def update_restaurant(request, id):
    """
    Update restaurant data page.
    Roure for 'management/r/<int:id>'.
    """
    query = Restaurant.objects.filter(id=id).first()
    if request.method == "POST":
        form = CreateRestaurant(request.POST, request.FILES, instance=query)
        if form.is_valid() and request.user == query.owner:
            form.save()
            messages.info(request, "Updated info")

            return redirect("management")
    fill = {
        "name": query.name,
        "address": query.address,
        "owner": query.owner,
        "description": query.description,
        "photo": query.photo,
    }
    form = CreateRestaurant(fill, instance=query)

    return render(request, "food/management_restaurant.html", {"form": form, "id": id})


@login_required(login_url="login")
def update_dish(request, id):
    """
    Update dish data page.
    Roure for 'management/d/<int:id>'.
    """
    if request.method == "POST":
        dish = Dish.objects.filter(id=id).first()
        form = CreateDish(request.POST, request.FILES, instance=dish)
        if form.is_valid() and request.user == dish.restaurant.owner:
            form.save()
            messages.info(request, "Updated dish")
    return redirect(f"/dish/{id}")


@login_required(login_url="login")
def delete_dish(request, id):
    """
    Delete restaurant.
    Roure for 'remove/r/<int:id>'.
    """
    dish = Dish.objects.get(id=id)
    rid = dish.restaurant.id
    dish.delete()
    messages.info(request, "Deleted")

    return redirect(f"/restaurant/{rid}")


@login_required(login_url="login")
def delete_restaurant(request, id):
    """
    Delete dish.
    Roure for 'remove/d/<int:id>'.
    """
    Restaurant.objects.get(id=id).delete()
    messages.info(request, "Deleted")

    return redirect(f"/management")


def get_cart(request):
    """
    Returns JSON data of the cart.
    Roure for 'get-cart'.
    """
    body = json.loads(request.body.decode("utf-8"))
    data = {}
    if "cart" in body:
        for item in body["cart"]:
            q = Dish.objects.get(id=int(item))
            if not q.id in data:
                data[q.id] = {
                    "id": q.id,
                    "quantity": body["cart"][item],
                    "name": q.name,
                    "price": float(q.price),
                    "photo": q.photo.url,
                }
            else:
                data[q.id]["quantity"] += 1
    else:
        return JsonResponse({"error": "no cart in request"})

    return JsonResponse(data)


@login_required(login_url="login")
def set_order_status(request):
    """
    Sets status of the order.
    Roure for 'order-status'.
    """
    body = json.loads(request.body.decode("utf-8"))
    id_, status = (
        int(body["id"]),
        int(body["status"]),
    )
    Order.objects.get(id=id_).update(status=status)
    return JsonResponse({"ok": True})


def address(request):
    """
    Creates an order.
    Roure for 'address'.
    """
    if request.method == "POST":
        form = CreateOrder(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Congratulations. Order completed")
            if not request.user.id:
                return redirect("home")
            return redirect("management")
        messages.info(request, "Something went wrong.")

    form = CreateOrder()
    return render(request, "food/address.html", {"form": form})


def restaurant_orders(request, id):
    """
    Lists all of the orders placed at the restaurant.
    Route for 'restaurant/<int:id>/orders'
    """
    restaurant = Restaurant.objects.get(id=id)
    restaurant_dishes = Dish.objects.filter(restaurant=restaurant)
    ids = [f"{d.id}" for d in restaurant_dishes]
    orders = Order.objects.filter(dishes__has_keys=ids)

    orders_obj = get_orders(orders)
    return render(request, "food/orders_restaurant.html", {"orders": orders_obj})


def get_orders(obj):
    """
    Function for creating a dictionary of the given dishes.
    """
    orders_list = []
    for order in obj:
        total = 0.0
        dishes = []
        for id_ in order.dishes:
            dish_ = Dish.objects.get(id=int(id_))
            total += float(dish_.price) * order.dishes[id_]
            dishes.append(
                {
                    "price": float(dish_.price),
                    "quantity": order.dishes[id_],
                    "photo": dish_.photo.url,
                    "name": dish_.name,
                    "id": dish_.id,
                }
            )
        orders_list.append(
            {
                "id": order.id,
                "region": order.region_address,
                "city": order.city_address,
                "street": order.street_address,
                "zip": order.zip_code,
                "dishes": dishes,
                "total": total,
                "status": order.status,
            }
        )
    return orders_list
