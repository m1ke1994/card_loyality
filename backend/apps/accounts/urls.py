from django.urls import include, path
from rest_framework import routers

from .admin_views import StaffViewSet

from . import views

router = routers.DefaultRouter()
router.register(r"admin/staff", StaffViewSet, basename="staff")

urlpatterns = [
    path("me", views.MeView.as_view()),
    path("me/visits", views.MyVisitsView.as_view()),
    path("me/transactions", views.MyTransactionsView.as_view()),
    path("me/coupons", views.MyCouponsView.as_view()),
    path("staff/me", views.StaffMeView.as_view()),
    path("staff/places", views.StaffPlacesView.as_view()),
    path("points/adjust", views.PointsAdjustView.as_view()),
    path("", include(router.urls)),
]
