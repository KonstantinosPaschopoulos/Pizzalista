from django.views.generic import TemplateView
from django.urls import path

from . import views

app_name = "pizza"
urlpatterns = [
    path(
        "about",
        TemplateView.as_view(template_name="pizza/base_about.html"),
        name="about",
    ),
    path("", views.index_view, name="index"),
    path("city-guide/<slug:slug>/", views.city_guide_view, name="city-guide"),
    path("search", views.index_search_view, name="index-search"),
    path("my/favorites", views.FavoritesListView.as_view(), name="favorites-list"),
    path("my/visits", views.PizzeriaVisitListView.as_view(), name="visits-list"),
    path("my/wishlist", views.WishlistListView.as_view(), name="wishlist-list"),
    path("my/ratings", views.RatingsListView.as_view(), name="ratings-list"),
    path("my/reviews", views.ReviewsListView.as_view(), name="reviews-list"),
    path("pizzeria/<int:pk>", views.pizzeria_detail_view, name="pizzeria-detail"),
    path(
        "pizzeria/<int:pizzeria_id>/toggle-wishlist",
        views.toggle_wishlist,
        name="toggle-wishlist",
    ),
    path(
        "pizzeria/<int:pizzeria_id>/toggle-favorite",
        views.toggle_favorite,
        name="toggle-favorite",
    ),
    path("pizzeria/<int:pizzeria_id>/add-visit", views.add_visit, name="add-visit"),
    path(
        "pizzeria/<int:pizzeria_id>/rate/<int:rating_value>",
        views.rate,
        name="rate",
    ),
    path(
        "pizzeria/<int:pizzeria_id>/rate-delete",
        views.rate_delete,
        name="rate-delete",
    ),
    path(
        "pizzeria/<int:pizzeria_id>/review-form",
        views.review_form_view,
        name="review-form",
    ),
    path(
        "pizzeria/<int:pizzeria_id>/delete-review",
        views.delete_review_view,
        name="delete-review",
    ),
]
