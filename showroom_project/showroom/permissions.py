from rest_framework import permissions


class IsClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_client


class IsShowroomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_showroom


class IsProviderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_provider


class CanEditPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.can_edit
