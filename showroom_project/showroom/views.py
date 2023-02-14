# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import (
    CarFilter,
    ClientFilter,
    ProviderFilter,
    SaleHistoryFilter,
    ShowroomFilter,
)
from .models import Car, Client, Provider, SaleHistory, Showroom
from .permissions import (
    CanEditPermission,
    IsClientPermission,
    IsProviderPermission,
    IsShowroomPermission,
)
from .serializers import (
    CarSerializer,
    ClientSerializer,
    ProviderSerializer,
    SaleHistorySerializer,
    ShowroomSerializer,
)


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    queryset = Car.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated, CanEditPermission]

        return super(CarViewSet, self).get_permissions()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter
    permission_classes = [permissions.IsAuthenticated, IsClientPermission]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ShowroomViewSet(viewsets.ModelViewSet):
    queryset = Showroom.objects.all()
    serializer_class = ShowroomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShowroomFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated, CanEditPermission]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super(ShowroomViewSet, self).get_permissions()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = SaleHistory.objects.all()
    serializer_class = SaleHistorySerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SaleHistoryFilter

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProviderFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated, CanEditPermission]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super(ProviderViewSet, self).get_permissions()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
