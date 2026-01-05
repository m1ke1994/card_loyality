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
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=32)),
                ("type", models.CharField(choices=[("percent", "Percent"), ("fixed", "Fixed"), ("gift", "Gift"), ("free_item", "Free Item")], max_length=32)),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                ("conditions_json", models.JSONField(default=dict)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
                ("max_uses", models.IntegerField(default=0)),
                ("uses_count", models.IntegerField(default=0)),
                ("status", models.CharField(default="active", max_length=32)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="coupons", to="tenants.tenant")),
            ],
            options={"db_table": "coupons", "ordering": ["id"], "unique_together": {("tenant", "code")}},
        ),
        migrations.CreateModel(
            name="UserCoupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(default="active", max_length=32)),
                ("coupon", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="user_coupons", to="coupons.coupon")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="user_coupons", to="accounts.user")),
            ],
            options={"db_table": "user_coupons", "unique_together": {("coupon", "user")}},
        ),
    ]
