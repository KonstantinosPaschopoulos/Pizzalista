from django.shortcuts import render
from pizza.models import Pizzeria


def pizzeria_map_view(request):
    pizzerias = Pizzeria.objects.exclude(latitude__isnull=True).exclude(
        longitude__isnull=True
    )
    pizzerias_data = [
        {
            "name": pizzeria.name,
            "latitude": pizzeria.latitude,
            "longitude": pizzeria.longitude,
            "profile_picture": pizzeria.profile_picture.url,
            "address": pizzeria.address,
            "url": pizzeria.get_absolute_url(),
        }
        for pizzeria in pizzerias
    ]
    return render(
        request, "maps/base_index_map.html", context={"locations": list(pizzerias_data)}
    )
