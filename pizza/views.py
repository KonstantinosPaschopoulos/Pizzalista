from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from .models import (
    Pizzeria,
    PizzeriaVisit,
    Wishlist,
    Favorite,
    Review,
    Rating,
    MIN_RATING,
    MAX_RATING,
)
from base.models import City


# LIST VIEWS

PAGINATION_N = 10


@require_GET
def index_view(request):
    context = {
        "milan_pizzerias": Pizzeria.objects.filter(city__name="Milan", hot_slice=True)[
            :4
        ]
    }
    return render(request, "pizza/base_index.html", context)


@require_GET
def index_search_view(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("pizza:index")

    pizzeria_list = Pizzeria.objects.filter(
        Q(name__icontains=query) | Q(address__icontains=query)
    )
    paginator = Paginator(pizzeria_list, PAGINATION_N)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "pizza/base_search.html", {"page_obj": page_obj, "query": query}
    )


@require_GET
def city_guide_view(request, slug: str):
    city: City = get_object_or_404(City, slug=slug)
    context: dict = {
        "pizzerias": Pizzeria.objects.filter(city=city),
        "city": city,
    }
    return render(request, "pizza/base_city_guide.html", context)


class PizzeriaVisitListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATION_N
    template_name = "pizza/base_personal_pizzeria_list.html"
    http_method_names = ["get"]

    def get_queryset(self):
        return PizzeriaVisit.objects.filter(user=self.request.user)


class WishlistListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATION_N
    template_name = "pizza/base_personal_pizzeria_list.html"
    http_method_names = ["get"]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class FavoritesListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATION_N
    template_name = "pizza/base_personal_pizzeria_list.html"
    http_method_names = ["get"]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class RatingsListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATION_N
    template_name = "pizza/base_personal_pizzeria_list.html"
    http_method_names = ["get"]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


class ReviewsListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATION_N
    template_name = "pizza/base_personal_pizzeria_list.html"
    http_method_names = ["get"]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


# PIZZERIA DETAIL VIEW


def _get_rating_context(rating=None):
    return {
        "rating_value": rating.rating if rating else 0,
        "rating_list": range(MIN_RATING, MAX_RATING + 1),
    }


@require_GET
def pizzeria_detail_view(request, pk):
    pizzeria = get_object_or_404(Pizzeria, pk=pk)
    context = {"pizzeria": pizzeria}

    if request.user.is_authenticated:
        user_visits = PizzeriaVisit.objects.filter(user=request.user, pizzeria=pizzeria)
        context["user_visits"] = user_visits
        context["has_visited_today"] = user_visits.filter(
            visit_date=timezone.now().date()
        ).exists()

        context["has_wishlist"] = Wishlist.objects.filter(
            user=request.user, pizzeria=pizzeria
        ).exists()
        context["is_favorite"] = Favorite.objects.filter(
            user=request.user, pizzeria=pizzeria
        ).exists()
        context["review"] = Review.objects.filter(
            user=request.user, pizzeria=pizzeria
        ).first()

        context.update(
            _get_rating_context(
                Rating.objects.filter(user=request.user, pizzeria=pizzeria).first()
            )
        )
    return render(request, "pizza/base_pizzeria.html", context)


# ACTIONS


@login_required
@require_POST
def toggle_wishlist(request, pizzeria_id):
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, pizzeria=pizzeria
    )
    if not created:
        wishlist_item.delete()

    return render(
        request,
        "pizza/base_pizzeria_wishlist.html",
        {"pizzeria": pizzeria, "has_wishlist": created},
    )


@login_required
@require_POST
def toggle_favorite(request, pizzeria_id):
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)

    favorite_item, created = Favorite.objects.get_or_create(
        user=request.user, pizzeria=pizzeria
    )
    if not created:
        favorite_item.delete()

    return render(
        request,
        "pizza/base_pizzeria_favorite.html",
        {"pizzeria": pizzeria, "is_favorite": created},
    )


@login_required
@require_POST
def add_visit(request, pizzeria_id):
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)

    visit_date = timezone.now().date()
    if not PizzeriaVisit.objects.filter(
        user=request.user, pizzeria=pizzeria, visit_date=visit_date
    ).exists():
        PizzeriaVisit.objects.create(
            user=request.user, pizzeria=pizzeria, visit_date=visit_date
        )

    return HttpResponse("<p>You have successfully tracked your visit today!</p>")


@login_required
@require_POST
def rate(request, pizzeria_id, rating_value):
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)

    rating, _ = Rating.objects.get_or_create(
        user=request.user, pizzeria=pizzeria, defaults={"rating": rating_value}
    )
    rating.rating = rating_value
    rating.save()

    context = {"pizzeria": pizzeria}
    context.update(_get_rating_context(rating))

    return render(request, "pizza/base_pizzeria_ratings.html", context)


@login_required
@require_POST
def rate_delete(request, pizzeria_id):
    # TODO: Handle all the 404s gracefully.
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)
    if rating := Rating.objects.filter(user=request.user, pizzeria=pizzeria).first():
        rating.delete()

    context = {"pizzeria": pizzeria}
    context.update(_get_rating_context())

    return render(request, "pizza/base_pizzeria_ratings.html", context)


@login_required
def review_form_view(request, pizzeria_id):
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)
    review = Review.objects.filter(user=request.user, pizzeria=pizzeria).first()
    context = {"pizzeria": pizzeria}

    if request.method == "POST" and (review_text := request.POST.get("review_text")):
        if review:
            review.review_text = review_text
            review.save()
        else:
            review = Review.objects.create(
                user=request.user, pizzeria=pizzeria, review_text=review_text
            )
        context["submitted"] = True
    context["review"] = review

    return render(request, "pizza/base_pizzeria_review_section.html", context)


@login_required
def delete_review_view(request, pizzeria_id):
    pizzeria = get_object_or_404(Pizzeria, pk=pizzeria_id)
    if review := Review.objects.filter(user=request.user, pizzeria=pizzeria).first():
        review.delete()

    context = {"pizzeria": pizzeria}
    return render(request, "pizza/base_pizzeria_review_section.html", context)
