from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.models import LoyaltyAccount, User
from apps.accounts.utils import generate_token, hash_token, issue_tokens_for_user, verify_hashed
from apps.tenants.models import Tenant
from .models import TelegramLoginSession


class TelegramSessionStartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.headers.get("X-Bot-Token") != settings.TELEGRAM_BOT_TOKEN:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        tenant_slug = request.data.get("tenant_slug")
        telegram_user_id = request.data.get("telegram_user_id")
        chat_id = request.data.get("chat_id")
        display_name = request.data.get("display_name", "")
        if not (tenant_slug and telegram_user_id):
            return Response({"detail": "Missing tenant_slug or telegram_user_id"}, status=400)
        try:
            tenant = Tenant.objects.get(slug=tenant_slug, status="active")
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found"}, status=404)

        raw_token = generate_token(16)
        token_hash = hash_token(raw_token)
        expires_at = timezone.now() + timezone.timedelta(seconds=settings.LOGIN_TOKEN_TTL_SEC)
        TelegramLoginSession.objects.create(
            tenant=tenant,
            telegram_user_id=telegram_user_id,
            chat_id=chat_id,
            display_name=display_name,
            login_token_hash=token_hash,
            expires_at=expires_at,
        )
        return Response({"login_token": raw_token, "expires_at": expires_at})


class TelegramConsumeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        tenant_slug = request.data.get("tenant_slug")
        if not (token and tenant_slug):
            return Response({"detail": "Missing token or tenant_slug"}, status=400)
        try:
            tenant = Tenant.objects.get(slug=tenant_slug, status="active")
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found"}, status=404)

        sessions = TelegramLoginSession.objects.filter(
            tenant=tenant, used_at__isnull=True, expires_at__gt=timezone.now()
        ).order_by("-created_at")
        session = None
        for candidate in sessions:
            if verify_hashed(token, candidate.login_token_hash):
                session = candidate
                break
        if not session:
            return Response({"detail": "Invalid or expired token"}, status=400)

        user, _ = User.objects.get_or_create(
            tenant=tenant,
            telegram_user_id=session.telegram_user_id,
            defaults={"telegram_chat_id": session.chat_id, "display_name": session.display_name},
        )
        LoyaltyAccount.objects.get_or_create(user=user)
        session.used_at = timezone.now()
        session.save(update_fields=["used_at"])
        tokens = issue_tokens_for_user(user)
        return Response(tokens)


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Invalid token"}, status=400)
        return Response({"detail": "Logged out"})
