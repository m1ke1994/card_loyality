from django.db import models
from apps.tenants.models import Tenant


class AuditLog(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="audit_logs")
    actor_type = models.CharField(max_length=32)
    actor_id = models.CharField(max_length=64)
    action = models.CharField(max_length=64)
    entity = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=64)
    meta_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
