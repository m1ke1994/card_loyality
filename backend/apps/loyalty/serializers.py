from rest_framework import serializers

from .models import IssuedToken, Transaction, Visit


class IssuedTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedToken
        fields = ["jti", "expires_at"]


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["id", "place", "started_at", "ended_at", "amount_total", "points_earned", "points_spent", "status"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "type", "points", "amount", "meta_json", "created_at"]
