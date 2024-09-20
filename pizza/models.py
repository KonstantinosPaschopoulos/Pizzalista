from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Coalesce, Lower
from django.db.models import Q
from base.models import City


MIN_RATING = 1
MAX_RATING = 8


class PizzaCategory(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_pizza_category")
        ]
        ordering = ["name"]


class Pizzeria(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    pizza_categories = models.ManyToManyField(PizzaCategory)
    profile_picture = models.ImageField(
        default="default_pizzeria.jpg",
        upload_to="pizzeria_profile_pictures/",
        blank=True,
    )
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hot_slice = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} in {self.address}"

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), "address", name="unique_pizzeria")
        ]
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("pizza:pizzeria-detail", kwargs={"pk": self.pk})

    @property
    def rating_count(self):
        return self.rating_set.count()

    @property
    def average_rating(self):
        avg_rating = self.rating_set.aggregate(
            avg=Coalesce(
                models.Avg("rating"), models.Value(0), output_field=models.FloatField()
            )
        )["avg"]

        return round(avg_rating, 1)


class PizzeriaVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizzeria = models.ForeignKey(Pizzeria, on_delete=models.CASCADE)
    visit_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "pizzeria", "visit_date"], name="unique_pizzeria_visit"
            )
        ]
        ordering = ["-visit_date"]


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizzeria = models.ForeignKey(Pizzeria, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=255)
    last_update = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "pizzeria"], name="unique_review")
        ]
        ordering = ["-last_update"]


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizzeria = models.ForeignKey(Pizzeria, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "pizzeria"], name="unique_wishlist")
        ]
        ordering = ["-create_date"]


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizzeria = models.ForeignKey(Pizzeria, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "pizzeria"], name="unique_favorite")
        ]
        ordering = ["-create_date"]


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizzeria = models.ForeignKey(Pizzeria, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )
    last_update = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "pizzeria"], name="unique_rating"),
            models.CheckConstraint(
                check=Q(rating__gte=MIN_RATING) & Q(rating__lte=MAX_RATING),
                name="rating_range_check",
            ),
        ]
        ordering = ["-last_update"]
