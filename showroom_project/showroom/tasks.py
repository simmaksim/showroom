import decimal
import json

from django.db.models import Q
from showroom_project.celery import app

from .models import (
    Client,
    Provider,
    ProviderCar,
    ProviderSaleHistory,
    ProviderSales,
    Showroom,
    ShowroomCar,
    ShowroomSaleHistory,
    ShowroomSales,
)

app.conf.timezone = "UTC"


def check_sale_showroom(showroom, car):
    for sale in ShowroomSales.objects.all():
        return sale if sale.showroom == showroom and sale.car == car else None


def create_deal(showroom, client, car):

    if car.cars_count != 0:
        sale = check_sale_showroom(showroom=car.showroom, car=car.car).sale
        if sale is not None:
            price = car.price * decimal.Decimal(str(1 - (sale / 100)))
        else:
            price = car.price

        showroom.balance += price
        client.balance -= price
        car.cars_count -= 1
        ShowroomSaleHistory(
            price=price, car_id=car.car.id, client_id=client.id, showroom_id=showroom.id
        ).save()
        showroom.save()
        client.save()
        car.save()


@app.task()
def client_buy_car_from_showroom():
    match = False
    available_cars = []
    for client in Client.objects.all():
        for showroom in Showroom.objects.all():
            if client.location == showroom.location:
                client_on_deal = client
                showroom_on_deal = showroom
                match = True
    for showroom_car in ShowroomCar.objects.all():
        if showroom_car.showroom == showroom_on_deal:
            available_cars.append(showroom_car)
    if match:
        for car in available_cars:
            create_deal(showroom_on_deal, client_on_deal, car)


def check_sale_provider(provider, car):
    for sale in ProviderSales.objects.all():
        return sale if sale.provider == provider and sale.car == car else None


@app.task
def showroom_buy_car():
    for showroom in Showroom.objects.all():
        # for item in showroom.criteries:
        #     if item is None:
        #         buy_all = True
        # if not buy_all:
        #     provider_cars = ProviderCar.objects.all()
        # else:
        #     cars_matched_criteries = (
        #         Q(car__brand__startswith=showroom.criteries.get("brand"))
        #         & Q(car__power__exact=showroom.criteries.get("power"))
        #         & Q(car__color__startswith=showroom.criteries.get("color"))
        #         & Q(car__body__startswith=showroom.criteries.get("body"))
        #     )
        #     provider_cars = ProviderCar.objects.filter(cars_matched_criteries)
        # if showroom.criteries != {}
        data_filter_conditions = {}
        data = json.loads(showroom.criteries)
        for key in data:
            if data[key]:
                data_filter_conditions[f"car__{key}__icontains"] = data[key]
        q = Q(**data_filter_conditions)
        provider_cars = ProviderCar.objects.filter(q)
        for provider_car in provider_cars:
            if provider_car.cars_count != 0:
                if (
                    check_sale_provider(provider_car.provider, provider_car.car)
                    is not None
                ):
                    sale = (
                        check_sale_provider(
                            provider=provider_car.provider, car=provider_car.car
                        ).sale
                        / 100
                    )
                else:
                    sale = 0
                price = provider_car.price * decimal.Decimal(str(1 - sale))
                showroom.balance -= price
                provider = Provider.objects.get(id=provider_car.provider.id)
                showroom_car, created = ShowroomCar.objects.get_or_create(
                    car_id=provider_car.car.id, showroom_id=showroom.id, price=price
                )
                if created:
                    showroom_car.cars_count = 0
                else:
                    showroom_car.cars_count += 1

                provider.balance += price
                provider_car.cars_count -= 1
                ProviderSaleHistory(
                    price=price,
                    car_id=provider_car.car.id,
                    provider_id=provider.id,
                    showroom_id=showroom.id,
                ).save()
                showroom.save()
                provider.save()
                provider_car.save()
                showroom_car.save()
