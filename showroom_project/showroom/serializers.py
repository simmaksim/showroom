from rest_framework import serializers

from .models import Car, SaleHistory, Showroom, User


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "year",
            "brand",
            "model",
            "image",
            "vin",
            "power",
            "color",
            "body",
            "is_active",
            "created",
            "updated",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "surname", "balance", "location", "created", "updated"]


class ShowroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showroom
        fields = [
            "name",
            "location",
            "balance",
            "unique_users",
            "criteries",
            "is_active",
            "created",
            "updated",
        ]


class SaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleHistory
        fields = ["price", "car", "user", "showroom", "created", "updated"]
