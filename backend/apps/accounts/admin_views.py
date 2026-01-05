from rest_framework import viewsets

from apps.accounts.permissions import IsTenantAdmin
from apps.tenants.models import Place
from .models import Staff, StaffPlace, User
from .serializers import StaffSerializer


class StaffViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantAdmin]
    serializer_class = StaffSerializer

    def get_queryset(self):
        return Staff.objects.select_related("user").filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        telegram_user_id = self.request.data.get("telegram_user_id")
        display_name = self.request.data.get("display_name", "")
        user, _ = User.objects.get_or_create(
            tenant=self.request.user.tenant,
            telegram_user_id=telegram_user_id,
            defaults={"display_name": display_name, "role": "staff"},
        )
        user.role = "staff"
        user.save(update_fields=["role", "display_name"])
        staff = Staff.objects.create(tenant=user.tenant, user=user, role=self.request.data.get("role", "staff"))
        place_ids = self.request.data.get("place_ids", [])
        for pid in place_ids:
            place = Place.objects.get(id=pid, tenant=user.tenant)
            StaffPlace.objects.create(staff=staff, place=place)
        serializer.instance = staff
