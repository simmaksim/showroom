from django_filters import CharFilter, FilterSet, ModelChoiceFilter, NumberFilter

from .models import Car, Client, Provider, SaleHistory, Showroom


class CarFilter(FilterSet):
    year = NumberFilter(field_name="year", lookup_expr="exact")
    brand = CharFilter(field_name="brand", lookup_expr="exact")
    model = CharFilter(field_name="model", lookup_expr="exact")
    vin = CharFilter(field_name="vin", lookup_expr="exact")
    power = NumberFilter(field_name="power", lookup_expr="exact")
    color = CharFilter(field_name="color", lookup_expr="exact")
    body = CharFilter(field_name="body", lookup_expr="exact")

    class Meta:
        model = Car
        fields = ["year", "brand", "model", "vin", "power", "color", "body"]


class ClientFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    surname = CharFilter(field_name="surname", lookup_expr="icontains")
    balance = NumberFilter(field_name="balance", lookup_expr="exact")
    location = CharFilter(field_name="location", lookup_expr="exact")

    class Meta:
        model = Client
        fields = ["name", "surname", "balance", "location"]


class ShowroomFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    location = CharFilter(field_name="location", lookup_expr="exact")
    balance = NumberFilter(field_name="balance", lookup_expr="exact")
    unique_clients = ModelChoiceFilter(
        field_name="unique_clients", queryset=Client.objects.all()
    )

    class Meta:
        model = Showroom
        fields = ["name", "location", "balance", "unique_clients"]


class SaleHistoryFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    car = CharFilter(field_name="car__name", lookup_expr="iexact")
    client = CharFilter(field_name="client__name", lookup_expr="iexact")
    showroom = CharFilter(field_name="showroom__name", lookup_expr="iexact")

    class Meta:
        model = SaleHistory
        fields = ["min_price", "max_price", "car", "client", "showroom"]


class ProviderFilter(FilterSet):
    min_clients_count = NumberFilter(field_name="clients_count", lookup_expr="gte")
    max_clients_count = NumberFilter(field_name="clients_count", lookup_expr="lte")
    name = CharFilter(lookup_expr="icontains")
    location = CharFilter(lookup_expr="iexact")
    car = CharFilter(field_name="cars__name", lookup_expr="iexact")

    class Meta:
        model = Provider
        fields = ["min_clients_count", "max_clients_count", "name", "location", "car"]
