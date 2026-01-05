from django.db import models

from apps.tenants.models import Tenant


class Promotion(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="promotions")
    name = models.CharField(max_length=255)
    rules_json = models.JSONField(default=dict)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, default="active")

    class Meta:
        db_table = "promotions"
        ordering = ["id"]
