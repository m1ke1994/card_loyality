from django.db import models

from apps.tenants.models import Tenant
from apps.accounts.models import User


class Coupon(models.Model):
    TYPES = (("percent", "Percent"), ("fixed", "Fixed"), ("gift", "Gift"), ("free_item", "Free Item"))

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="coupons")
    code = models.CharField(max_length=32)
    type = models.CharField(max_length=32, choices=TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    conditions_json = models.JSONField(default=dict)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.IntegerField(default=0)
    uses_count = models.IntegerField(default=0)
    status = models.CharField(max_length=32, default="active")

    class Meta:
        db_table = "coupons"
        ordering = ["id"]
        unique_together = ("tenant", "code")


class UserCoupon(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="user_coupons")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_coupons")
    assigned_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, default="active")

    class Meta:
        db_table = "user_coupons"
        unique_together = ("coupon", "user")
