from rest_framework import viewsets

from apps.accounts.permissions import IsTenantAdmin
from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantAdmin]
    serializer_class = PlaceSerializer

    def get_queryset(self):
        return Place.objects.filter(tenant=self.request.user.tenant)
