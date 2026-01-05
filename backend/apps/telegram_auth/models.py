from django.db import models

from apps.tenants.models import Tenant


class TelegramLoginSession(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="telegram_login_sessions")
    telegram_user_id = models.BigIntegerField()
    chat_id = models.BigIntegerField(null=True, blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    login_token_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "telegram_login_sessions"
        ordering = ["-created_at"]
