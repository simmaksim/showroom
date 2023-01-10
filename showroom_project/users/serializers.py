from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "is_showroom",
            "is_provider",
            "is_client",
            "username",
            "date_joined",
            "is_active",
        ]
