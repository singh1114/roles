from rest_framework.permissions import BasePermission


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and "USER" in [group.name for group in request.user.groups.all()]:
            return True


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and "ADMIN" in [group.name for group in request.user.groups.all()]:
            return True


class IsSuperAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and "SUPERADMIN" in [group.name for group in request.user.groups.all()]:
            return True
