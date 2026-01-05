from django.urls import include, path
from rest_framework import routers

from .views import PlaceViewSet

router = routers.DefaultRouter()
router.register(r"admin/places", PlaceViewSet, basename="place")

urlpatterns = [path("", include(router.urls))]
