from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "telegram_chat_id",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
