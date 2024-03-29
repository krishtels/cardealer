import uuid

from django.contrib.auth.models import AbstractUser
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from tools.models import BaseModel, Discount


class User(AbstractUser):
    class Profile(models.TextChoices):
        NONE = "none"
        CUSTOMER = "customer"
        SHOWROOM = "showroom"
        PROVIDER = "provider"

    user_type = models.CharField(
        choices=Profile.choices, max_length=8, default=Profile.NONE
    )

    def __str__(self):
        return self.username


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


class Customer(BaseModel):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Provider(BaseModel):
    name = models.CharField(max_length=100)
    year_founded = models.DateField(null=True)
    unique_customers_amount = models.IntegerField(default=0)
    cars = models.ManyToManyField(Car, through="ProviderCars")
    country = CountryField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    price_with_discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        null=True,
    )

    def save(self, percent=None, *args, **kwargs):
        if percent:
            self.price_with_discount = self.price * (100 - percent) / 100
        else:
            self.price_with_discount = self.price
        super().save(*args, **kwargs)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    price_with_discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        null=True,
    )

    def save(self, percent=None, *args, **kwargs):
        if percent:
            self.price_with_discount = self.price * (100 - percent) / 100
        else:
            self.price_with_discount = self.price
        super().save(*args, **kwargs)

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


class CarShowroomDiscount(Discount):
    showroom = models.ForeignKey(CarShowroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ProviderDiscount(Discount):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
