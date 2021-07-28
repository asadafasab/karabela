from django.contrib import admin

from .models import Restaurant, Dish, OpinionDish, OpinionRestaurant

admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(OpinionDish)
admin.site.register(OpinionRestaurant)
