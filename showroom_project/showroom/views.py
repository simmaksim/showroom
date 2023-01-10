# Create your views here.
from django.shortcuts import render
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, SaleHistory, Showroom, User
from .serializers import (CarSerializer, SaleHistorySerializer,
                          ShowroomSerializer, UserSerializer)


class CarList(APIView):
    serializer_class = CarSerializer

    def get(self, request, format=None):
        cars = Car.objects.all()

        # #serializer = CarSerializer(cars)
        # print(serializer.data)
        # return Response(serializer.data)
        try:
            serializer = self.serializer_class(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:

            return Response(status=status.HTTP_502_BAD_GATEWAY)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDetail(APIView):
    serializer_class = CarSerializer

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


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ShowroomList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Showroom.objects.all()
    serializer_class = ShowroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ShowroomDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Showroom.objects.all()
    serializer_class = ShowroomSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = SaleHistory.objects.all()
    serializer_class = SaleHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
