from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="country_unique_lower_name")
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    header_image = models.ImageField(upload_to="city_images/", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), "country", name="city_unique_lower_name_country"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.country.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.country.name}")
        super().save(*args, **kwargs)
