from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=32, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tenants"
        ordering = ["id"]

    def __str__(self):
        return self.slug


class TenantDomain(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="domains")
    domain = models.CharField(max_length=255, unique=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tenant_domains"
        ordering = ["id"]

    def __str__(self):
        return f"{self.domain} ({self.tenant.slug})"


class Place(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=64, default="Europe/Moscow")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "places"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} ({self.tenant.slug})"
