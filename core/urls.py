from django.urls import include, path
from rest_framework import routers

from core.views import (
    CarShowroomDiscountViewSet,
    CarShowroomSalesHistoryViewSet,
    CarShowroomViewSet,
    CarViewSet,
    CustomerViewSet,
    ProviderDiscountDetailView,
    ProviderDiscountListView,
    ProviderSalesHistoryViewSet,
    ProviderViewSet, UserViewSet,
)

router = routers.DefaultRouter()
router.register("cars", CarViewSet)
router.register("showrooms", CarShowroomViewSet)
router.register("customers", CustomerViewSet)
router.register("providers", ProviderViewSet)
router.register("showroomdiscounts", CarShowroomDiscountViewSet)
router.register("showroomsaleshistory", CarShowroomSalesHistoryViewSet)
router.register("providersaleshistory", ProviderSalesHistoryViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "providerdiscounts/<int:pk>/",
        ProviderDiscountDetailView.as_view(),
        name="providerdiscountdetail",
    ),
    path(
        "providerdiscounts/",
        ProviderDiscountListView.as_view(),
        name="providerdiscountslist",
    ),
]
