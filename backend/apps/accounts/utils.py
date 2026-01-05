import secrets
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken


def issue_tokens_for_user(user):
    refresh = RefreshToken()
    refresh["uid"] = user.id
    refresh["tid"] = user.tenant_id
    access = refresh.access_token
    access["uid"] = user.id
    access["tid"] = user.tenant_id
    return {"access": str(access), "refresh": str(refresh)}


def generate_token(length=32):
    return secrets.token_urlsafe(length)


def hash_token(token: str):
    return make_password(token)


def verify_hashed(token: str, token_hash: str) -> bool:
    return check_password(token, token_hash)


def now_utc():
    return datetime.now(timezone.utc)


def expires_in(seconds: int):
    return now_utc() + timedelta(seconds=seconds)
