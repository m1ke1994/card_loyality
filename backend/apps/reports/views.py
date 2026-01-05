from django.db.models import Count, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsTenantAdmin
from apps.loyalty.models import Transaction, Visit
from apps.tenants.models import Place


class SummaryReportView(APIView):
    permission_classes = [IsTenantAdmin]

    def get(self, request):
        visits_count = Visit.objects.filter(tenant=request.user.tenant).count()
        transactions_count = Transaction.objects.filter(tenant=request.user.tenant).count()
        points_earned = (
            Transaction.objects.filter(tenant=request.user.tenant, type="earn").aggregate(total=Sum("points"))["total"]
            or 0
        )
        points_spent = (
            Transaction.objects.filter(tenant=request.user.tenant, type="spend").aggregate(total=Sum("points"))["total"]
            or 0
        )
        return Response(
            {
                "visits": visits_count,
                "transactions": transactions_count,
                "points_earned": points_earned,
                "points_spent": points_spent,
            }
        )


class VisitsReportView(APIView):
    permission_classes = [IsTenantAdmin]

    def get(self, request):
        data = (
            Visit.objects.filter(tenant=request.user.tenant)
            .values("place__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return Response(list(data))


class TransactionsReportView(APIView):
    permission_classes = [IsTenantAdmin]

    def get(self, request):
        data = (
            Transaction.objects.filter(tenant=request.user.tenant)
            .values("type")
            .annotate(count=Count("id"), points=Sum("points"))
            .order_by("-count")
        )
        return Response(list(data))
