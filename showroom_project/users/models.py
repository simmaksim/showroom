from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    is_showroom = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.is_showroom} {self.is_provider} {self.is_client} {self.username} {self.date_joined} {self.is_active}"
