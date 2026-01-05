from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telegram_user_id", models.BigIntegerField()),
                ("telegram_chat_id", models.BigIntegerField(blank=True, null=True)),
                ("display_name", models.CharField(blank=True, max_length=255)),
                ("role", models.CharField(choices=[("user", "User"), ("staff", "Staff"), ("tenant_admin", "Tenant Admin"), ("superadmin", "Super Admin")], default="user", max_length=32)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="users", to="tenants.tenant")),
            ],
            options={"db_table": "users", "ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(default="staff", max_length=32)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staff_members", to="tenants.tenant")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="staff_profile", to="accounts.user")),
            ],
            options={"db_table": "staff", "ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="StaffPlace",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("place", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="place_staff", to="tenants.place")),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staff_places", to="accounts.staff")),
            ],
            options={"db_table": "staff_places", "unique_together": {("staff", "place")}},
        ),
        migrations.CreateModel(
            name="LoyaltyAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("points_balance_cache", models.IntegerField(default=0)),
                ("tier", models.CharField(choices=[("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold")], default="bronze", max_length=16)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="loyalty_account", to="accounts.user")),
            ],
            options={"db_table": "loyalty_accounts"},
        ),
        migrations.AlterUniqueTogether(name="user", unique_together={("tenant", "telegram_user_id")}),
    ]
