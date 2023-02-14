import json

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from users.factories import AdminUserFactory, CustomUserFactory, ProviderUserFactory

from .factories import CarFactory, ClientFactory, ProviderFactory, ShowroomFactory
from .models import Car, Client, Provider, Showroom
from .views import ClientViewSet, ShowroomViewSet

CARS_ENDPOINT = "/cars/"
CLIENT_ENDPOINT = "/clients/"
SHOWROOM_ENDPOINT = "/showrooms/"
PROVIDER_ENDPOINT = "/providers/"
SALEHISTORY_ENDPOINT = "/salehistory/"


class CarViewSetTestCase(APITestCase):
    def setUp(self):
        self.cars = [CarFactory() for i in range(3)]
        self.user2 = CustomUserFactory()
        self.admin_user2 = AdminUserFactory()
        self.provider_user = ProviderUserFactory()
        self.data = {
            "year": 2020,
            "brand": "Tesla",
            "model": "modelx",
            "image": "https://hdpic.club/uploads/posts/2021-12/1640254737_1-hdpic-club-p-folksvagen-polo-krasivie-1.jpg",
            "vin": "JH4DA9380PS016488",
            "power": 200,
            "color": "WH",
            "body": "SE",
            "is_active": True,
        }

    def test_list_car(self):
        response = self.client.get(f"{CARS_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["results"][0]["year"], self.cars[0].year)
        self.assertEqual(response.data["results"][0]["brand"], self.cars[0].brand)
        self.assertEqual(response.data["results"][0]["model"], self.cars[0].model)
        self.assertEqual(response.data["results"][0]["image"], self.cars[0].image)
        self.assertEqual(response.data["results"][0]["vin"], self.cars[0].vin)
        self.assertEqual(response.data["results"][0]["color"], self.cars[0].color)
        self.assertEqual(response.data["results"][0]["body"], self.cars[0].body)
        self.assertEqual(
            response.data["results"][0]["is_active"], self.cars[0].is_active
        )

    def test_create_car_as_admin(self):
        self.client.force_authenticate(user=self.admin_user2)
        response = self.client.post(
            f"{CARS_ENDPOINT}",
            data=self.data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 4)

    def test_car_bad_request(self):
        self.client.force_authenticate(user=self.admin_user2)
        response = self.client.post(
            f"{CARS_ENDPOINT}", data=self.data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Car.objects.count(), 3)

    def test_post_car_provider(self):
        self.client.force_authenticate(user=self.provider_user)
        response = self.client.post(
            f"{CARS_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 4)

    def test_car_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        data = {
            "year": 2020,
            "brand": "BMW",
            "model": "X5",
            "image": "https://www.example.com/bmw_x5.jpg",
            "vin": "12345678901234",
            "power": 600,
            "color": "BL",
        }
        response = self.client.post(f"{CARS_ENDPOINT}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Car.objects.count(), 3)

    def test_put_request_by_admin(self):
        self.client.force_authenticate(user=self.admin_user2)
        response = self.client.put(
            f"{CARS_ENDPOINT}{self.cars[0].id}/", self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_car_delete_request(self):
        self.client.force_authenticate(user=self.admin_user2)
        car = Car.objects.create(
            year=2020,
            brand="Toyota",
            model="Camry",
            image="https://example.com/camry.jpg",
            vin="12345678901234567",
            power=200,
            color="Black",
        )
        response = self.client.delete(f"{CARS_ENDPOINT}{car.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Car.objects.get(pk=car.id).is_active)


class ClientViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ClientViewSet.as_view(actions={"get": "list"})
        self.user = CustomUserFactory()
        self.provider_user = ProviderUserFactory()
        self.admin_user = AdminUserFactory()
        self.app_client = ClientFactory(
            name="Maksim", surname="Slizh", balance=1000, location="BL"
        )
        self.data = {
            "name": "Maksim",
            "surname": "Slizh",
            "balance": 1000,
            "location": "BL",
            "is_active": True,
        }
        self.bad_data = {
            "name": "Maksim",
            "surname": "Slizh",
            "balance": 1000,
            "location": "BL",
            "is_active": True,
        }

    def test_get_client_list_unauthenticated(self):
        request = self.factory.get(f"{CLIENT_ENDPOINT}")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_client_list_authenticated(self):
        request = self.factory.get(f"{CLIENT_ENDPOINT}")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "Maksim")

    def test_post_client_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"{CLIENT_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 2)

    def test_post_client_unauthenticated(self):
        response = self.client.post(
            f"{CLIENT_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 1)

    def test_post_client_bad_request(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"{CLIENT_ENDPOINT}", data=self.bad_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Client.objects.count(), 1)

    def test_post_client_default_user(self):
        self.client.force_authenticate(user=self.provider_user)
        response = self.client.post(
            f"{CLIENT_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Client.objects.count(), 1)

    def test_client_delete_request(self):
        self.client.force_authenticate(user=self.admin_user)
        client = Client.objects.create(
            name="Maksim",
            surname="Slizh",
            balance=1000,
            location="BL",
            is_active=True,
        )
        response = self.client.delete(f"{CLIENT_ENDPOINT}{client.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Client.objects.get(pk=client.id).is_active)


class ShowroomViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ShowroomViewSet.as_view(actions={"get": "list"})
        self.car = CarFactory()
        self.user = CustomUserFactory()
        self.admin_user = AdminUserFactory()
        self.client_app = ClientFactory(
            name="Maksim", surname="Slizh", balance=1000, location="BL"
        )
        self.showroom = ShowroomFactory(
            name="Atlant",
            location="BL",
            balance=5000,
            unique_clients=self.client_app,
            criteries={
                "year": "2001",
                "brand": "Toyota",
                "model": "Camry",
                "power": 200,
                "color": "BL",
                "body": "UN",
            },
        )
        self.showroom.cars.set([self.car])

    def test_showroom_get_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f"{SHOWROOM_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["results"][0]["name"], "Atlant")

    def test_showroom_get_unauthenticated(self):
        response = self.client.get(f"{SHOWROOM_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data), 1)

    def test_showroom_delete_request(self):
        self.client.force_authenticate(user=self.admin_user)
        showroom = Showroom.objects.create(
            name="Atlant",
            location="BL",
            balance=5000,
            unique_clients=self.client_app,
            criteries={
                "year": "2001",
                "brand": "Toyota",
                "model": "Camry",
                "power": 200,
                "color": "BL",
                "body": "UN",
            },
        )
        response = self.client.delete(f"{SHOWROOM_ENDPOINT}{showroom.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Showroom.objects.get(pk=showroom.id).is_active)

    # def test_post_showroom_authenticated(self):
    #     self.client.force_authenticate(user=self.admin_user)
    #     data = {
    #         "name": "string",
    #         "location": "AF",
    #         "balance": "5000",
    #         "unique_clients": self.client_app,
    #         "is_active": True,
    #     }
    #     response = self.client.post(
    #         f"{SHOWROOM_ENDPOINT}",
    #         data=json.dumps(data),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Client.objects.count(), 0)


class ProviderViewSetTest(APITestCase):
    def setUp(self):
        self.car = CarFactory()
        self.user = CustomUserFactory()
        self.admin_user = AdminUserFactory()
        self.provider_user = ProviderUserFactory()
        self.provider = ProviderFactory(name="Seva", clients_count=0, location="BL")
        self.provider.cars.set([self.car])
        self.data = {
            "name": "string",
            "clients_count": 2147483647,
            "location": "AF",
            "is_active": True,
        }

    def test_provider_get_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f"{PROVIDER_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["results"][0]["name"], "Seva")

    def test_provider_get_authenticated(self):
        self.client.force_authenticate(user=self.provider_user)
        response = self.client.get(f"{PROVIDER_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["results"][0]["name"], "Seva")

    def test_provider_get_unauthenticated(self):
        response = self.client.get(f"{PROVIDER_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data), 1)

    def test_post_provider_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"{PROVIDER_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 0)

    def test_post_provider_unauthenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f"{PROVIDER_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Client.objects.count(), 0)

    def test_post_provider_unauthenticated(self):
        response = self.client.post(
            f"{PROVIDER_ENDPOINT}",
            data=json.dumps(self.data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 0)

    def test_delete_provider_request(self):
        self.client.force_authenticate(user=self.admin_user)
        provider = Provider.objects.create(
            name="string",
            clients_count=2147483647,
            location="AF",
            is_active=True,
        )
        response = self.client.delete(f"{PROVIDER_ENDPOINT}{provider.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Provider.objects.get(pk=provider.id).is_active)


class TestSaleHistoryViewSet(APITestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.admin_user = AdminUserFactory()
        self.salehistory = {"price": 100000, "car": 0, "provider": 0, "showroom": 0}

    def test_salehistory_get_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f"{SALEHISTORY_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["count"], 0)

    def test_salehistory_get_unauthenticated(self):
        response = self.client.get(f"{SALEHISTORY_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data), 1)
