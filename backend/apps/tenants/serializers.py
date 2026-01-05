from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

    def create(self, validated_data):
        validated_data["tenant"] = self.context["request"].user.tenant
        return super().create(validated_data)
