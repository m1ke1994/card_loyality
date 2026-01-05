from rest_framework import serializers

from .models import Coupon, UserCoupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

    def create(self, validated_data):
        validated_data["tenant"] = self.context["request"].user.tenant
        return super().create(validated_data)


class UserCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCoupon
        fields = "__all__"
