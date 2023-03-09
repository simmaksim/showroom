# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .filters import (
    CarFilter,
    ClientFilter,
    ProviderFilter,
    ProviderSaleHistoryFilter,
    ShowroomFilter,
    ShowroomSaleHistoryFilter,
)
from .models import (
    Car,
    Client,
    Provider,
    ProviderSaleHistory,
    Showroom,
    ShowroomSaleHistory,
)
from .permissions import CanEditPermission, IsClientPermission
from .serializers import (
    CarSerializer,
    ClientSerializer,
    ProviderSaleHistorySerializer,
    ProviderSerializer,
    ShowroomSaleHistorySerializer,
    ShowroomSerializer,
)


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    queryset = Car.objects.all()

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


class ShowroomSaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = ShowroomSaleHistory.objects.all()
    serializer_class = ShowroomSaleHistorySerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShowroomSaleHistoryFilter

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProviderSaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = ProviderSaleHistory.objects.all()
    serializer_class = ProviderSaleHistorySerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProviderSaleHistoryFilter

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
