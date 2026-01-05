from django.db import models
from django.utils import timezone

from apps.tenants.models import Place, Tenant
from apps.accounts.models import User


class Transaction(models.Model):
    TYPES = (("earn", "Earn"), ("spend", "Spend"), ("adjust", "Adjust"), ("refund", "Refund"))

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="transactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    visit = models.ForeignKey("Visit", on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    type = models.CharField(max_length=16, choices=TYPES)
    points = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    meta_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]


class Visit(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("closed", "Closed"))

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="visits")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name="visits")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points_earned = models.IntegerField(default=0)
    points_spent = models.IntegerField(default=0)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="active")

    class Meta:
        db_table = "visits"
        ordering = ["-started_at"]


class ActiveVisit(models.Model):
    STATUS_CHOICES = (("locked", "Locked"), ("closed", "Closed"))

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="active_visits")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="active_visit")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="active_visits")
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="locked")

    class Meta:
        db_table = "active_visits"


class IssuedToken(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="issued_tokens")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issued_tokens")
    jti = models.CharField(max_length=128, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    used_place_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "issued_tokens"
        ordering = ["-created_at"]

    def is_valid(self):
        return self.used_at is None and timezone.now() < self.expires_at
