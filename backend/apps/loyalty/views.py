import uuid

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import LoyaltyAccount, User
from apps.accounts.permissions import IsStaff
from apps.accounts.serializers import UserSerializer
from apps.tenants.models import Place
from .models import ActiveVisit, IssuedToken, Transaction, Visit


def redis_lock(key: str, ttl: int = 5):
    redis = get_redis_connection()
    lock = redis.lock(key, timeout=ttl)
    return lock


class TokenIssueView(APIView):
    def post(self, request):
        jti = uuid.uuid4().hex
        expires_at = timezone.now() + timezone.timedelta(seconds=settings.QR_TOKEN_TTL_SEC)
        IssuedToken.objects.create(
            tenant=request.user.tenant,
            user=request.user,
            jti=jti,
            expires_at=expires_at,
        )
        return Response({"qr_token": jti, "expires_at": expires_at})


class TokenVerifyView(APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        token = request.data.get("token")
        place_id = request.data.get("place_id")
        if not (token and place_id):
            return Response({"detail": "token and place_id required"}, status=400)
        try:
            record = IssuedToken.objects.select_related("user").get(jti=token)
        except IssuedToken.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=404)
        if record.user.tenant_id != request.user.tenant_id:
            return Response({"detail": "Cross-tenant denied"}, status=403)
        if not record.is_valid():
            return Response({"detail": "Token expired or used"}, status=400)

        lock = redis_lock(f"qr_token:{token}")
        if not lock.acquire(blocking=False):
            return Response({"detail": "Token race, retry"}, status=429)
        try:
            with transaction.atomic():
                record.refresh_from_db()
                if not record.is_valid():
                    return Response({"detail": "Token expired or used"}, status=400)
                active_visit = ActiveVisit.objects.filter(user=record.user, status="locked").first()
                if active_visit and active_visit.place_id != int(place_id):
                    return Response({"detail": "User active in another place"}, status=409)
                place = Place.objects.get(id=place_id, tenant=request.user.tenant, is_active=True)
                visit = Visit.objects.filter(user=record.user, status="active").order_by("-started_at").first()
                if not active_visit:
                    active_visit = ActiveVisit.objects.create(
                        tenant=request.user.tenant, user=record.user, place=place
                    )
                    visit = Visit.objects.create(
                        tenant=request.user.tenant,
                        user=record.user,
                        place=place,
                        status="active",
                    )
                if visit and visit.status == "closed":
                    visit = Visit.objects.create(tenant=request.user.tenant, user=record.user, place=place, status="active")
                record.used_at = timezone.now()
                record.used_place_id = place.id
                record.save(update_fields=["used_at", "used_place_id"])
        finally:
            lock.release()

        return Response(
            {
                "status": "ok",
                "user": UserSerializer(record.user).data,
                "active_place_id": active_visit.place_id,
                "visit_id": visit.id if "visit" in locals() and visit else None,
            }
        )


class CheckoutView(APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        visit_id = request.data.get("visit_id")
        amount_total = float(request.data.get("amount_total", 0))
        points_spent = int(request.data.get("points_spent", 0))
        coupon_code = request.data.get("coupon_code")
        try:
            visit = Visit.objects.select_for_update().get(id=visit_id, tenant=request.user.tenant)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found"}, status=404)
        with transaction.atomic():
            visit.amount_total = amount_total
            visit.points_spent = points_spent
            earned = int(amount_total * 0.05)
            visit.points_earned = earned
            visit.ended_at = timezone.now()
            visit.status = "closed"
            visit.save()

            account, _ = LoyaltyAccount.objects.get_or_create(user=visit.user)
            account.adjust(earned - points_spent)
            if earned:
                Transaction.objects.create(
                    tenant=visit.tenant,
                    user=visit.user,
                    place=visit.place,
                    visit=visit,
                    type="earn",
                    points=earned,
                    amount=amount_total,
                    meta_json={"by": request.user.id},
                )
            if points_spent:
                Transaction.objects.create(
                    tenant=visit.tenant,
                    user=visit.user,
                    place=visit.place,
                    visit=visit,
                    type="spend",
                    points=-points_spent,
                    amount=amount_total,
                    meta_json={"coupon": coupon_code, "by": request.user.id},
                )
            ActiveVisit.objects.filter(user=visit.user).update(status="closed")
        return Response({"status": "closed", "points_earned": earned})
