from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("actor_type", models.CharField(max_length=32)),
                ("actor_id", models.CharField(max_length=64)),
                ("action", models.CharField(max_length=64)),
                ("entity", models.CharField(max_length=64)),
                ("entity_id", models.CharField(max_length=64)),
                ("meta_json", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="audit_logs", to="tenants.tenant")),
            ],
            options={"db_table": "audit_logs", "ordering": ["-created_at"]},
        ),
    ]
