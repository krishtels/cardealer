import uuid

from django.contrib.auth.models import AbstractUser
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from tools.models import BaseModel, Sale


class Car(models.Model):
    class EngineType(models.TextChoices):
        Gasoline = "Gasoline"
        Diesel = "Diesel"
        Hybrid = "Hybrid"
        Electric = "Electric"

    engine_type = models.CharField(
        choices=EngineType.choices, max_length=20, default=EngineType.Gasoline
    )
    brand = models.CharField(null=True, max_length=20)
    model = models.CharField(null=True, max_length=20)
    color = models.CharField(null=True, max_length=20)
    engine_volume = models.FloatField(validators=[MinValueValidator(0.00)], default=0.0)

    def __str__(self):
        return f"{self.brand}-{self.model}"

    class Meta:
        unique_together = [
            "brand",
            "model",
            "color",
            "engine_volume",
            "engine_type",
        ]


class Customer(AbstractUser):
    class Gender(models.TextChoices):
        M = "Male"
        F = "Female"

    sex = models.CharField(choices=Gender.choices, max_length=6)
    phone_number = PhoneNumberField(null=True, unique=True)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )
    age = models.IntegerField(null=True, validators=[MinValueValidator(18)])
    country = CountryField(null=True)
    specification = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Provider(BaseModel):
    name = models.CharField(max_length=100)
    year_founded = models.DateField(null=True)
    unique_customers_amount = models.IntegerField(default=0)
    cars = models.ManyToManyField(Car, through="ProviderCars")
    country = CountryField(null=True)

    def __str__(self):
        return f"{self.name}"


class ProviderCars(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )

    class Meta:
        unique_together = ("car", "provider")


class CarShowroom(BaseModel):
    name = models.CharField(max_length=100)
    country = CountryField(null=True)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )
    cars = models.ManyToManyField(Car, through="ShowroomCars")
    specification = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    def __str__(self):
        return f"{self.name}"


class ShowroomCars(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    showroom = models.ForeignKey(CarShowroom, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )

    class Meta:
        unique_together = ("car", "showroom")


class CarShowroomSalesHistory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    showroom = models.ForeignKey(CarShowroom, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )
    amount = models.IntegerField(default=0)


class ProviderSalesHistory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    showroom = models.ForeignKey(CarShowroom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )


class CarShowroomDiscount(Sale):
    showroom = models.ForeignKey(CarShowroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ProviderDiscount(Sale):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
