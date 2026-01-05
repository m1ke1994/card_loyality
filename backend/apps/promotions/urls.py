from django.urls import include, path
from rest_framework import routers

from .views import PromotionViewSet

router = routers.DefaultRouter()
router.register(r"admin/promotions", PromotionViewSet, basename="promotion")

urlpatterns = [path("", include(router.urls))]
