from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loyalty.models import Transaction, Visit
from apps.coupons.models import UserCoupon
from apps.tenants.models import Place
from .models import LoyaltyAccount, Staff, StaffPlace, User
from .permissions import IsStaff
from .serializers import (
    LoyaltyAccountSerializer,
    PlaceSerializer,
    StaffPlaceSerializer,
    StaffSerializer,
    UserSerializer,
)


class MeView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MyVisitsView(APIView):
    def get(self, request):
        visits = Visit.objects.filter(user=request.user).order_by("-started_at")[:100]
        data = [
            {
                "id": v.id,
                "place": v.place.name if v.place else None,
                "started_at": v.started_at,
                "ended_at": v.ended_at,
                "amount_total": v.amount_total,
                "points_earned": v.points_earned,
                "points_spent": v.points_spent,
                "status": v.status,
            }
            for v in visits
        ]
        return Response(data)


class MyTransactionsView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by("-created_at")[:200]
        data = [
            {
                "id": t.id,
                "type": t.type,
                "points": t.points,
                "amount": t.amount,
                "meta": t.meta_json,
                "created_at": t.created_at,
            }
            for t in transactions
        ]
        return Response(data)


class MyCouponsView(APIView):
    def get(self, request):
        coupons = (
            UserCoupon.objects.select_related("coupon")
            .filter(user=request.user)
            .order_by("-assigned_at")[:100]
        )
        data = [
            {
                "code": uc.coupon.code,
                "type": uc.coupon.type,
                "value": uc.coupon.value,
                "status": uc.status,
                "assigned_at": uc.assigned_at,
                "used_at": uc.used_at,
            }
            for uc in coupons
        ]
        return Response(data)


class StaffMeView(APIView):
    permission_classes = [IsStaff]

    def get(self, request):
        staff = request.user.staff_profile
        serializer = StaffSerializer(staff)
        places = PlaceSerializer(
            Place.objects.filter(place_staff__staff=staff, is_active=True), many=True
        )
        return Response({"staff": serializer.data, "places": places.data})


class StaffPlacesView(generics.ListAPIView):
    permission_classes = [IsStaff]
    serializer_class = PlaceSerializer

    def get_queryset(self):
        staff = self.request.user.staff_profile
        return Place.objects.filter(place_staff__staff=staff, is_active=True)


class PointsAdjustView(APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        target_user_id = request.data.get("user_id")
        points = int(request.data.get("points", 0))
        reason = request.data.get("reason", "")
        try:
            target_user = User.objects.get(id=target_user_id, tenant=request.user.tenant)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        account, _ = LoyaltyAccount.objects.get_or_create(user=target_user)
        account.adjust(points)
        Transaction.objects.create(
            tenant=target_user.tenant,
            user=target_user,
            place=None,
            visit=None,
            type="adjust",
            points=points,
            amount=0,
            meta_json={"reason": reason, "by_staff": request.user.id},
        )
        return Response({"balance": account.points_balance_cache})
