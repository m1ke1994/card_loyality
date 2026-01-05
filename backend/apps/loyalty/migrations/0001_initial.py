from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Visit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("ended_at", models.DateTimeField(blank=True, null=True)),
                ("amount_total", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("points_earned", models.IntegerField(default=0)),
                ("points_spent", models.IntegerField(default=0)),
                ("status", models.CharField(choices=[("active", "Active"), ("closed", "Closed")], default="active", max_length=32)),
                ("place", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="visits", to="tenants.place")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="visits", to="tenants.tenant")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="visits", to="accounts.user")),
            ],
            options={"db_table": "visits", "ordering": ["-started_at"]},
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(choices=[("earn", "Earn"), ("spend", "Spend"), ("adjust", "Adjust"), ("refund", "Refund")], max_length=16)),
                ("points", models.IntegerField()),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("meta_json", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("place", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="transactions", to="tenants.place")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="transactions", to="tenants.tenant")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="transactions", to="accounts.user")),
                ("visit", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="transactions", to="loyalty.visit")),
            ],
            options={"db_table": "transactions", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="IssuedToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("jti", models.CharField(max_length=128, unique=True)),
                ("expires_at", models.DateTimeField()),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("used_place_id", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issued_tokens", to="tenants.tenant")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issued_tokens", to="accounts.user")),
            ],
            options={"db_table": "issued_tokens", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ActiveVisit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("last_activity_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(choices=[("locked", "Locked"), ("closed", "Closed")], default="locked", max_length=32)),
                ("place", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="active_visits", to="tenants.place")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="active_visits", to="tenants.tenant")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="active_visit", to="accounts.user")),
            ],
            options={"db_table": "active_visits"},
        ),
    ]
