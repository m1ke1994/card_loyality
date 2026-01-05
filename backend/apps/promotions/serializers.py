from rest_framework import serializers

from .models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

    def create(self, validated_data):
        validated_data["tenant"] = self.context["request"].user.tenant
        return super().create(validated_data)
