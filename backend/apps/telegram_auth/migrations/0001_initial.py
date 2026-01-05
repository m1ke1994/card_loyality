from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramLoginSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telegram_user_id", models.BigIntegerField()),
                ("chat_id", models.BigIntegerField(blank=True, null=True)),
                ("display_name", models.CharField(blank=True, max_length=255)),
                ("login_token_hash", models.CharField(max_length=255)),
                ("expires_at", models.DateTimeField()),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="telegram_login_sessions", to="tenants.tenant")),
            ],
            options={"db_table": "telegram_login_sessions", "ordering": ["-created_at"]},
        ),
    ]
