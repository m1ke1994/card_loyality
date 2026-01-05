from django.urls import include, path
from rest_framework import routers

from .views import CouponViewSet

router = routers.DefaultRouter()
router.register(r"admin/coupons", CouponViewSet, basename="coupon")

urlpatterns = [path("", include(router.urls))]
