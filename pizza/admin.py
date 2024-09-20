from django.contrib import admin

from .models import (
    PizzaCategory,
    Pizzeria,
    PizzeriaVisit,
    Review,
    Wishlist,
    Favorite,
    Rating,
)

admin.site.register(
    [
        PizzaCategory,
        Pizzeria,
        PizzeriaVisit,
        Review,
        Wishlist,
        Favorite,
        Rating,
    ]
)
