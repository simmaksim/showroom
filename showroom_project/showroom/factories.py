import factory
from factory import Faker
from factory.django import DjangoModelFactory

from .models import Car, Client, Provider, Showroom


class CarFactory(DjangoModelFactory):

    year = factory.Faker("random_int", min=1940, max=2024)
    brand = factory.Faker(
        "random_element", elements=["VW", "Volvo", "Audi", "BMW", "Mercedes"]
    )
    model = factory.Faker("word")
    image = factory.Faker("url")
    vin = factory.Faker("ean13")
    power = factory.Faker("random_int", min=0, max=5000)
    color = factory.Faker("random_element", elements=["WH", "RE", "GR", "BL", "BK"])
    body = factory.Faker(
        "random_element", elements=["SE", "HB", "LB", "CO", "UN", "PU", "MV"]
    )

    class Meta:
        model = Car


class ClientFactory(DjangoModelFactory):

    name = Faker("first_name")
    surname = Faker("last_name")
    balance = factory.Faker("random_int", min=0, max=10000000)
    location = factory.Faker("country_code")

    class Meta:
        model = Client


class ShowroomFactory(DjangoModelFactory):
    name = Faker("Name")
    location = factory.Faker("country_code")
    balance = factory.Faker("random_int", min=0, max=10000000)
    unique_clients = factory.SubFactory(ClientFactory)
    criteries = {
        "year": factory.Faker("year"),
        "brand": factory.Faker("word"),
        "model": factory.Faker("word"),
        "power": factory.Faker("random_int", min=0, max=1000),
        "color": factory.Faker("color_name"),
        "body": factory.Faker("word"),
    }
    cars = factory.RelatedFactoryList(CarFactory)

    class Meta:
        model = Showroom


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    name = Faker("name")
    location = Faker("country_code")
    clients_count = Faker("random_int", min=0, max=1000)
    cars = factory.RelatedFactoryList(CarFactory)
