from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .models import User


class JWTAuthentication(BaseJWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("uid")
        tenant_id = validated_token.get("tid")
        if not user_id or not tenant_id:
            raise InvalidToken("Token missing uid/tid")
        try:
            return User.objects.select_related("tenant").get(id=user_id, tenant_id=tenant_id, is_active=True)
        except User.DoesNotExist as exc:
            raise InvalidToken("User not found or inactive") from exc
