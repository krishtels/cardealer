from django.contrib import admin

from .models import (
    Buyer,
    BuyerList,
    Car,
    CarList,
    CarPrice,
    Offer,
    SaleSeller,
    SaleShop,
    Seller,
    SellerHistory,
    SellerList,
    Shop,
    ShopHistory,
)

Models = (
    Buyer,
    BuyerList,
    Car,
    CarList,
    CarPrice,
    Shop,
    Offer,
    SaleSeller,
    SaleShop,
    Seller,
    SellerHistory,
    SellerList,
    ShopHistory,
)

admin.site.register(Models)
