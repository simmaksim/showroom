from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "is_showroom",
            "is_provider",
            "is_client",
            "username",
            "date_joined",
            "is_active",
            "can_edit",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        "username": "The username should only contain alphanumeric characters"
    }

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "is_showroom",
            "is_provider",
            "is_client",
            "can_edit",
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
