from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from tools.permissions import (
    IsCustomerAdminOrReadOnly,
    IsProviderAdmin,
    IsProviderAdminOrReadOnly,
    IsShowroomAdmin,
    IsShowroomAdminOrReadOnly,
)
from tools.validators import is_valid_id

from core.models import (
    Car,
    CarShowroom,
    CarShowroomDiscount,
    CarShowroomSalesHistory,
    Customer,
    Provider,
    ProviderCars,
    ProviderDiscount,
    ProviderSalesHistory,
    ShowroomCars,
    User,
)
from core.serializers import (
    CarSerializer,
    CarShowroomDiscountSerializer,
    CarShowroomSalesHistorySerializer,
    CarShowroomSerializer,
    CustomerSerializer,
    ProviderDiscountSerializer,
    ProviderSalesHistorySerializer,
    ProviderSerializer,
    UserSerializer,
)


class BaseViewSet(ModelViewSet):
    def perform_destroy(self, instance, pk=None):
        instance.is_active = False
        instance.save()


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsProviderAdminOrReadOnly,)


class CarShowroomViewSet(BaseViewSet):
    queryset = CarShowroom.objects.filter(is_active=True)
    serializer_class = CarShowroomSerializer
    permission_classes = (IsShowroomAdminOrReadOnly,)

    @action(
        detail=True,
        methods=["post"],
        url_path="add-car",
    )
    def add_showroom_cars(self, request, pk=None):
        showroom = self.get_object()
        car_id = request.data.get("car_id")
        if not is_valid_id(car_id):
            return Response(
                {"error": "Id must be numeric"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        car = get_object_or_404(Car, pk=car_id)

        amount = request.data.get("amount")
        price = request.data.get("price")
        try:
            ShowroomCars.objects.create(
                car=car, showroom=showroom, amount=amount, price=price
            )
        except IntegrityError:
            return Response(
                {"error": "This car already exists in this showroom"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)


class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    permission_classes = (IsCustomerAdminOrReadOnly,)


class ProviderViewSet(BaseViewSet):
    queryset = Provider.objects.filter(is_active=True)
    serializer_class = ProviderSerializer
    permission_classes = (IsProviderAdminOrReadOnly,)

    @action(
        detail=True,
        methods=["post"],
        url_path="add-car",
    )
    def add_provider_cars(self, request, pk=None):
        provider = self.get_object()
        car_id = request.data.get("car_id")
        if not is_valid_id(car_id):
            return Response(
                {"error": "Id must be numeric"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        car = get_object_or_404(Car, pk=car_id)

        price = request.data.get("price")
        try:
            ProviderCars.objects.create(car=car, provider=provider, price=price)
        except IntegrityError:
            return Response(
                {"error": "This car already exists in this provider"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)


class CarShowroomDiscountViewSet(BaseViewSet):
    queryset = CarShowroomDiscount.objects.filter(is_active=True)
    serializer_class = CarShowroomDiscountSerializer
    permission_classes = (
        IsShowroomAdminOrReadOnly,
    )


class ProviderDiscountListView(APIView):
    permission_classes = (IsProviderAdminOrReadOnly,)

    def get(self, request):
        discount = ProviderDiscount.objects.filter(is_active=True)
        serializer = ProviderDiscountSerializer(instance=discount, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderDiscountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProviderDiscountDetailView(APIView):
    permission_classes = (IsProviderAdminOrReadOnly,)

    def get(self, request, pk):
        discount = get_object_or_404(ProviderDiscount, pk=pk, is_active=True)
        serializer = ProviderDiscountSerializer(instance=discount)
        return Response(serializer.data)

    def put(self, request, pk):
        discount = get_object_or_404(ProviderDiscount, pk=pk, is_active=True)
        serializer = ProviderDiscountSerializer(
            instance=discount, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        discount = get_object_or_404(ProviderDiscount, pk=pk, is_active=True)
        discount.is_active = False
        discount.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarShowroomSalesHistoryViewSet(BaseViewSet):
    queryset = CarShowroomSalesHistory.objects.filter(is_active=True)
    serializer_class = CarShowroomSalesHistorySerializer
    permission_classes = (IsShowroomAdmin,)


class ProviderSalesHistoryViewSet(BaseViewSet):
    queryset = ProviderSalesHistory.objects.filter(is_active=True)
    serializer_class = ProviderSalesHistorySerializer
    permission_classes = (IsProviderAdmin,)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
