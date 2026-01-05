from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "role", "") in ("staff", "tenant_admin", "superadmin"))


class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "role", "") in ("tenant_admin", "superadmin"))
