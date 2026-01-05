from rest_framework import viewsets

from apps.accounts.permissions import IsTenantAdmin
from .models import Coupon
from .serializers import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantAdmin]
    serializer_class = CouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(tenant=self.request.user.tenant)
