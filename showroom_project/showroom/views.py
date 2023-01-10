# Create your views here.
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import (
    CarFilter,
    ClientFilter,
    ProviderFilter,
    SaleHistoryFilter,
    ShowroomFilter,
)
from .models import Car, Client, Provider, SaleHistory, Showroom
from .permissions import IsClientPermission, IsProviderPermission, IsShowroomPermission
from .serializers import (
    CarSerializer,
    ProviderSerializer,
    SaleHistorySerializer,
    ShowroomSerializer,
    UserSerializer,
)


class CarList(APIView):
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [
                permissions.IsAdminUser,
                IsShowroomPermission,
                IsProviderPermission,
            ]
        return super(CarViewSet, self).get_permissions()

    def get_object(self, pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_502_BAD_GATEWAY)

    def get(self, request, pk, format=None):
        cars = self.get_object(pk)
        serializer = self.serializer_class(
            cars,
        )
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cars = self.get_object(pk)
        serializer = self.serializer_class(
            cars,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter
    permission_classes = [permissions.IsAdminUser]


class ShowroomViewSet(viewsets.ModelViewSet):
    queryset = Showroom.objects.all()
    serializer_class = ShowroomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShowroomFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super(ShowroomViewSet, self).get_permissions()


class SaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = SaleHistory.objects.all()
    serializer_class = SaleHistorySerializer
    permission_classes = [
        IsClientPermission,
        IsShowroomPermission,
        permissions.IsAdminUser,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SaleHistoryFilter


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProviderFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super(ProviderViewSet, self).get_permissions()
