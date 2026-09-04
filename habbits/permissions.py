from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    "Доступ только для владельца объекта"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
