from rest_framework import viewsets

from apps.accounts.permissions import IsTenantAdmin
from .models import Promotion
from .serializers import PromotionSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantAdmin]
    serializer_class = PromotionSerializer

    def get_queryset(self):
        return Promotion.objects.filter(tenant=self.request.user.tenant)
