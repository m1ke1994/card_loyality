import threading

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from loyalty_saas.settings import TENANT_HEADER
from .models import Tenant

_local = threading.local()


def set_current_tenant(tenant):
    _local.tenant = tenant


def get_current_tenant():
    return getattr(_local, "tenant", None)


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        slug = request.headers.get("X-Tenant-Slug") or request.META.get(TENANT_HEADER)
        tenant = None
        if slug:
            try:
                tenant = Tenant.objects.get(slug=slug, status="active")
            except Tenant.DoesNotExist:
                return JsonResponse({"detail": "Invalid tenant"}, status=400)
        else:
            tenant = Tenant.objects.order_by("id").first()
        request.tenant = tenant
        set_current_tenant(tenant)

    def process_response(self, request, response):
        set_current_tenant(None)
        return response
