from django.db import models
from django.utils import timezone

from apps.tenants.models import Tenant, Place


class User(models.Model):
    ROLE = (("user", "User"), ("staff", "Staff"), ("tenant_admin", "Tenant Admin"), ("superadmin", "Super Admin"))

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
    telegram_user_id = models.BigIntegerField()
    telegram_chat_id = models.BigIntegerField(null=True, blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=32, choices=ROLE, default="user")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
        unique_together = ("tenant", "telegram_user_id")
        ordering = ["id"]

    def __str__(self):
        return f"{self.display_name or self.telegram_user_id} ({self.tenant.slug})"


class Staff(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="staff_members")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=32, default="staff")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "staff"
        ordering = ["id"]

    def __str__(self):
        return f"{self.user} [{self.role}]"


class StaffPlace(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="staff_places")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="place_staff")

    class Meta:
        db_table = "staff_places"
        unique_together = ("staff", "place")


class LoyaltyAccount(models.Model):
    TIER_CHOICES = (("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="loyalty_account")
    points_balance_cache = models.IntegerField(default=0)
    tier = models.CharField(max_length=16, choices=TIER_CHOICES, default="bronze")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "loyalty_accounts"

    def __str__(self):
        return f"{self.user_id} balance {self.points_balance_cache}"

    def adjust(self, delta: int):
        self.points_balance_cache = models.F("points_balance_cache") + delta
        self.save(update_fields=["points_balance_cache"])
        self.refresh_from_db()
        return self.points_balance_cache
