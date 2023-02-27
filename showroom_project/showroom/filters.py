from django_filters import CharFilter, FilterSet, ModelChoiceFilter, NumberFilter

from .models import (
    Car,
    Client,
    Provider,
    ProviderSaleHistory,
    Showroom,
    ShowroomSaleHistory,
)


class CarFilter(FilterSet):
    year = NumberFilter(field_name="year", lookup_expr="icontains")
    brand = CharFilter(field_name="brand", lookup_expr="icontains")
    model = CharFilter(field_name="model", lookup_expr="icontains")
    vin = CharFilter(field_name="vin", lookup_expr="exact")
    power = NumberFilter(field_name="power", lookup_expr="icontains")
    color = CharFilter(field_name="color", lookup_expr="icontains")
    body = CharFilter(field_name="body", lookup_expr="icontains")

    class Meta:
        model = Car
        fields = ["year", "brand", "model", "vin", "power", "color", "body"]


class ClientFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    surname = CharFilter(field_name="surname", lookup_expr="icontains")
    balance = NumberFilter(field_name="balance", lookup_expr="exact")
    location = CharFilter(field_name="location", lookup_expr="icontains")

    class Meta:
        model = Client
        fields = ["name", "surname", "balance", "location"]


class ShowroomFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    location = CharFilter(field_name="location", lookup_expr="icontains")
    balance = NumberFilter(field_name="balance", lookup_expr="exact")
    unique_clients = ModelChoiceFilter(
        field_name="unique_clients", queryset=Client.objects.all()
    )

    class Meta:
        model = Showroom
        fields = ["name", "location", "balance", "unique_clients"]


class ShowroomSaleHistoryFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    car = CharFilter(field_name="car__name", lookup_expr="icontains")
    client = CharFilter(field_name="client__name", lookup_expr="icontains")
    showroom = CharFilter(field_name="showroom__name", lookup_expr="icontains")

    class Meta:
        model = ShowroomSaleHistory
        fields = ["min_price", "max_price", "car", "client", "showroom"]


class ProviderSaleHistoryFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    car = CharFilter(field_name="car__name", lookup_expr="icontains")
    provider = CharFilter(field_name="provider__name", lookup_expr="icontains")
    showroom = CharFilter(field_name="showroom__name", lookup_expr="icontains")

    class Meta:
        model = ProviderSaleHistory
        fields = ["min_price", "max_price", "car", "provider", "showroom"]


class ProviderFilter(FilterSet):
    min_clients_count = NumberFilter(field_name="clients_count", lookup_expr="gte")
    max_clients_count = NumberFilter(field_name="clients_count", lookup_expr="lte")
    name = CharFilter(lookup_expr="icontains")
    location = CharFilter(lookup_expr="icontains")
    car = CharFilter(field_name="cars__name", lookup_expr="icontains")

    class Meta:
        model = Provider
        fields = ["min_clients_count", "max_clients_count", "name", "location", "car"]
