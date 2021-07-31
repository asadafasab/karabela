from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("signup", views.sign_up, name="signup"),
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("cart", views.cart, name="cart"),
    path("restaurants", views.restaurants, name="restaurants"),
    path("restaurant/<int:id>", views.restaurant, name="restaurant"),
    path(
        "restaurant/<int:id>/orders", views.restaurant_orders, name="restaurant orders"
    ),
    path("order-status", views.set_order_status, name="order status"),
    path("dish/<int:id>", views.dish, name="dish"),
    path("adddish", views.add_dish, name="add dish"),
    path("management", views.management, name="management"),
    path("management/r/<int:id>", views.update_restaurant, name="update restaurant"),
    path("management/d/<int:id>", views.update_dish, name="update dish"),
    path("remove/r/<int:id>", views.delete_restaurant, name="delete restaurant"),
    path("remove/d/<int:id>", views.delete_dish, name="delete dish"),
    path("get-cart", views.get_cart, name="get cart"),
    path("address", views.address, name="address"),
]
