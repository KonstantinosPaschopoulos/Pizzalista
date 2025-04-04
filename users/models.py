from django.db import models
from django.conf import settings


class ContactUs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.user.email
