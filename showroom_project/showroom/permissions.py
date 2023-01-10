from rest_framework import permissions


class IsClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_client and request.user.is_authenticated()


class IsShowroomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_showroom and request.user.is_authenticated()


class IsProviderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_provider and request.user.is_authenticated()
