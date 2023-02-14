from django.contrib.auth.models import AbstractUser, User
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):
    is_showroom = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.is_showroom} {self.is_provider} {self.is_client} {self.username} {self.date_joined} {self.is_active} {self.email} {self.can_edit}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
