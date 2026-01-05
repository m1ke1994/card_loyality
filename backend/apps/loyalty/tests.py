from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import LoyaltyAccount, Staff, User
from apps.accounts.utils import hash_token, issue_tokens_for_user
from apps.tenants.models import Place, Tenant
from apps.telegram_auth.models import TelegramLoginSession


class LoyaltyFlowTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test")
        self.place1 = Place.objects.create(tenant=self.tenant, name="P1")
        self.place2 = Place.objects.create(tenant=self.tenant, name="P2")
        self.user = User.objects.create(tenant=self.tenant, telegram_user_id=1, role="user")
        LoyaltyAccount.objects.create(user=self.user)
        self.staff_user = User.objects.create(tenant=self.tenant, telegram_user_id=2, role="staff")
        self.staff = Staff.objects.create(tenant=self.tenant, user=self.staff_user, role="staff")

    def auth_client(self, user):
        tokens = issue_tokens_for_user(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        return client

    def test_token_issue_and_verify(self):
        client_user = self.auth_client(self.user)
        resp = client_user.post("/api/v1/tokens/issue")
        self.assertEqual(resp.status_code, 200)
        qr_token = resp.data["qr_token"]

        client_staff = self.auth_client(self.staff_user)
        resp2 = client_staff.post("/api/v1/tokens/verify", {"token": qr_token, "place_id": self.place1.id})
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.data["status"], "ok")

    def test_active_visit_lock(self):
        client_user = self.auth_client(self.user)
        qr1 = client_user.post("/api/v1/tokens/issue").data["qr_token"]
        client_staff = self.auth_client(self.staff_user)
        client_staff.post("/api/v1/tokens/verify", {"token": qr1, "place_id": self.place1.id})
        qr2 = client_user.post("/api/v1/tokens/issue").data["qr_token"]
        resp = client_staff.post("/api/v1/tokens/verify", {"token": qr2, "place_id": self.place2.id})
        self.assertEqual(resp.status_code, 409)

    def test_telegram_consume(self):
        raw_token = "abc"
        from apps.accounts.utils import hash_token

        session = TelegramLoginSession.objects.create(
            tenant=self.tenant,
            telegram_user_id=12345,
            chat_id=6789,
            login_token_hash=hash_token(raw_token),
            expires_at=timezone.now() + timezone.timedelta(seconds=60),
        )
        client = APIClient()
        resp = client.post("/api/v1/auth/telegram/consume", {"token": raw_token, "tenant_slug": self.tenant.slug})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.data)
