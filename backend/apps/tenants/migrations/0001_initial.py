from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tenant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("status", models.CharField(default="active", max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "tenants", "ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="TenantDomain",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("domain", models.CharField(max_length=255, unique=True)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="domains", to="tenants.tenant"
                    ),
                ),
            ],
            options={"db_table": "tenant_domains", "ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Place",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("timezone", models.CharField(default="Europe/Moscow", max_length=64)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="places", to="tenants.tenant"
                    ),
                ),
            ],
            options={"db_table": "places", "ordering": ["id"]},
        ),
    ]
