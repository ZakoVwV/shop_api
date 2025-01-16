from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'last_name', 'first_name'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password_confirm != password:
            raise ValueError('password didn\'t match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(min_length=8, write_only=True, required=True)
    new_password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.pop('new_password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Passwords didn\'t match')
        return attrs