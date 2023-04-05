from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)


class Car(BaseModel):
    price = models.IntegerField()
    country = CountryField()
    characteristic = models.JSONField()


class Buyer(AbstractUser, BaseModel):
    phone_number = models.CharField(max_length=100)
    budget = models.IntegerField()


class Seller(BaseModel):
    name = models.CharField(max_length=100)
    year_founded = models.IntegerField()
    buyers_amount = models.IntegerField()
    car_prices = models.ManyToManyField(Car, through="CarPrice")


class Shop(BaseModel):
    name = models.CharField(max_length=100)
    country = CountryField()
    budget = models.IntegerField()
    car_list = models.ManyToManyField(Car, through="CarList")
    characteristic = models.JSONField()
    buyers_list = models.ManyToManyField(Buyer, through="BuyerList")
    sellers_list = models.ManyToManyField(Seller, through="SellerList")


class CarList(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount = models.IntegerField()


class BuyerList(BaseModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount_buy = models.IntegerField()


class ShopHistory(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField()


class Offer(BaseModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    max_price = models.IntegerField()


class SellerList(BaseModel):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    car = models.ManyToManyField(Car)


class SellerHistory(BaseModel):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.IntegerField()
    date = models.DateField()


class CarPrice(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.IntegerField()


class Sale(BaseModel):
    class Meta:
        abstract = True

    date_start = models.DateField()
    date_end = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount_to_get_sale = models.IntegerField()
    percent = models.IntegerField()


class SaleShop(Sale):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car)


class SaleSeller(Sale):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    shops = models.ManyToManyField(Shop)
    cars = models.ManyToManyField(Car)
