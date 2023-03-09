from rest_framework import serializers

from .models import (
    Car,
    Client,
    Provider,
    ProviderSaleHistory,
    Showroom,
    ShowroomSaleHistory,
)


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
        read_only_fields = ["is_active", "created", "updated"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "name",
            "surname",
            "balance",
            "location",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ["balance", "is_active", "created", "updated"]


class ShowroomSerializer(serializers.ModelSerializer):

    balance = serializers.FloatField(read_only=True)

    class Meta:
        model = Showroom
        fields = [
            "name",
            "location",
            "balance",
            "unique_clients",
            "criteries",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = [
            "balance",
            "is_active",
            "created",
            "updated",
        ]


class ShowroomSaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowroomSaleHistory
        fields = [
            "price",
            "car",
            "client",
            "showroom",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ["is_active", "created", "updated"]


class ProviderSaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderSaleHistory
        fields = [
            "price",
            "car",
            "showroom",
            "provider",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ["is_active", "created", "updated"]


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            "name",
            "clients_count",
            "location",
            "balance",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ["balance", "is_active", "created", "updated"]
