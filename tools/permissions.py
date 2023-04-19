from core.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProviderAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            user = request.user
            return user.is_authenticated and (
                (User.Profile.PROVIDER in user.user_type) or user.is_superuser
            )


class IsProviderAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            (User.Profile.PROVIDER in user.user_type) or user.is_superuser
        )


class IsShowroomAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            user = request.user
            return user.is_authenticated and (
                (User.Profile.SHOWROOM in user.user_type) or user.is_superuser
            )


class IsShowroomAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            (User.Profile.SHOWROOM in user.user_type) or user.is_superuser
        )


class IsCustomerAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            user = request.user
            return user.is_authenticated and (
                (User.Profile.CUSTOMER in user.user_type) or user.is_superuser
            )
