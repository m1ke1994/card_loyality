from rest_framework import serializers

from apps.tenants.models import Place
from .models import LoyaltyAccount, Staff, StaffPlace, User


class LoyaltyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyAccount
        fields = ["points_balance_cache", "tier", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    loyalty = LoyaltyAccountSerializer(source="loyalty_account", read_only=True)

    class Meta:
        model = User
        fields = ["id", "display_name", "telegram_user_id", "role", "loyalty"]


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "name", "address", "timezone", "is_active"]


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = ["id", "role", "is_active", "user"]


class StaffPlaceSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = StaffPlace
        fields = ["place"]
