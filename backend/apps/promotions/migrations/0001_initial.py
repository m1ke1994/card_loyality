from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promotion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("rules_json", models.JSONField(default=dict)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(default="active", max_length=32)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="promotions", to="tenants.tenant")),
            ],
            options={"db_table": "promotions", "ordering": ["id"]},
        ),
    ]
