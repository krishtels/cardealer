from datetime import date

from django.core.validators import MinValueValidator
from django.db.models import Count, F, Sum
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from core.models import (
    Car,
    CarShowroom,
    CarShowroomDiscount,
    CarShowroomSalesHistory,
    Customer,
    Provider,
    ProviderDiscount,
    ProviderSalesHistory,
    ShowroomCars,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "date_joined",
        )


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class SpecificationSerializer(serializers.Serializer):
    max_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0
    )
    engine_type = serializers.ChoiceField(
        choices=Car.EngineType.choices, default=Car.EngineType.Gasoline
    )
    brand = serializers.CharField(max_length=20, default=None)
    model = serializers.CharField(max_length=20, default=None)
    color = serializers.CharField(max_length=20, default=None)
    engine_volume = serializers.FloatField(
        validators=[MinValueValidator(0.00)], default=0.0
    )


class CarShowroomSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, required=False)
    specification = SpecificationSerializer(many=True, required=False)
    car_amount = serializers.SerializerMethodField()
    car_price = serializers.SerializerMethodField()
    car_price_with_discount = serializers.SerializerMethodField()

    country = CountryField(required=False)

    def get_car_amount(self, obj):
        showroom_cars = obj.showroomcars_set.all()
        return {car.car_id: car.amount for car in showroom_cars}

    def get_car_price(self, obj):
        showroom_cars = obj.showroomcars_set.all()
        return {car.car_id: car.price for car in showroom_cars}

    def get_car_price_with_discount(self, obj):
        showroom_cars = obj.showroomcars_set.all()
        return {car.car_id: car.price_with_discount for car in showroom_cars}

    class Meta:
        model = CarShowroom
        fields = [
            "id",
            "name",
            "country",
            "specification",
            "balance",
            "cars",
            "car_amount",
            "car_price",
            "user",
            "car_price_with_discount",
        ]
        read_only_fields = [
            "balance",
            "cars",
        ]


class CarShowroomNumberOfSellsSerializer(serializers.ModelSerializer):
    number_of_sales = serializers.SerializerMethodField()

    def get_number_of_sales(self, *args, **kwargs):
        return (
            CarShowroomSalesHistory.objects.filter(showroom=self.context["showroom_id"])
            .values("showroom")
            .annotate(Sum("amount"))
            .values_list("amount__sum", flat=True)[0]
        )

    class Meta:
        model = CarShowroom
        fields = ("number_of_sales",)


class CarShowroomProfitSerializer(serializers.ModelSerializer):
    profit = serializers.SerializerMethodField()

    def get_profit(self, *args, **kwargs):
        return (
            CarShowroomSalesHistory.objects.filter(showroom=self.context["showroom_id"])
            .values("showroom")
            .annotate(profit_sum=Sum(F("amount") * F("price")))
            .values_list("profit_sum", flat=True)[0]
        )

    class Meta:
        model = CarShowroom
        fields = ("profit",)


class CarShowroomUniqueCustomersSerializer(serializers.ModelSerializer):
    unique_customers = serializers.SerializerMethodField()

    def get_unique_customers(self, *args, **kwargs):
        return (
            CarShowroomSalesHistory.objects.filter(showroom=self.context["showroom_id"])
            .values_list("customer__user__username", flat=True)
            .distinct()
        )

    class Meta:
        model = CarShowroom
        fields = ("unique_customers",)


class CarShowroomUniqueProvidersSerializer(serializers.ModelSerializer):
    unique_providers = serializers.SerializerMethodField()

    def get_unique_providers(self, *args, **kwargs):
        return (
            ProviderSalesHistory.objects.filter(showroom=self.context["showroom_id"])
            .values_list("provider__name", flat=True)
            .distinct()
        )

    class Meta:
        model = CarShowroom
        fields = ("unique_providers",)


class CustomerSerializer(serializers.ModelSerializer):
    country = CountryField()
    specification = SpecificationSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = [
            "id",
            "country",
            "specification",
            "sex",
            "phone_number",
            "balance",
            "age",
            "user",
        ]
        read_only_fields = ["balance"]


class CustomerSpentMoneySerializer(serializers.ModelSerializer):
    spent_money = serializers.SerializerMethodField()

    def get_spent_money(self, *args, **kwargs):
        return (
            CarShowroomSalesHistory.objects.values("customer")
            .annotate(spent_sum=Sum(F("amount") * F("price")))
            .order_by("-spent_sum")
        )

    class Meta:
        model = Customer
        fields = ("spent_money",)


class ProviderSerializer(serializers.ModelSerializer):
    country = CountryField()
    cars = CarSerializer(many=True, required=False)
    car_price = serializers.SerializerMethodField()
    car_price_with_discount = serializers.SerializerMethodField()

    def get_car_price(self, obj):
        provider_cars = obj.providercars_set.all()
        return {car.car_id: car.price for car in provider_cars}

    def get_car_price_with_discount(self, obj):
        showroom_cars = obj.providercars_set.all()
        return {car.car_id: car.price_with_discount for car in showroom_cars}

    class Meta:
        model = Provider
        fields = [
            "name",
            "year_founded",
            "unique_customers_amount",
            "cars",
            "country",
            "car_price",
            "user",
            "car_price_with_discount",
        ]
        read_only_fields = [
            "unique_customers_amount",
            "cars",
        ]


class CarShowroomDiscountSerializer(serializers.ModelSerializer):
    params = SpecificationSerializer()

    def validate(self, data):
        if date.today() <= data["date_start"] <= data["date_end"]:
            return data
        else:
            raise serializers.ValidationError(
                {"end_date": "end date should be greater that start date"}
            )

    class Meta:
        model = CarShowroomDiscount
        fields = "__all__"


class ProviderDiscountSerializer(serializers.ModelSerializer):
    params = SpecificationSerializer()

    def validate(self, data):
        if date.today() <= data["date_start"] <= data["date_end"]:
            return data
        else:
            raise serializers.ValidationError(
                {"end_date": "end date should be greater that start date"}
            )

    class Meta:
        model = ProviderDiscount
        fields = "__all__"


class CarShowroomSalesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShowroomSalesHistory
        fields = (
            "id",
            "showroom",
            "car",
            "price",
            "amount",
            "created",
        )
        read_only_field = ["created"]


class ProviderSalesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderSalesHistory
        fields = (
            "id",
            "showroom",
            "car",
            "provider",
            "price",
            "amount",
            "created",
        )
        read_only_field = ["created"]
