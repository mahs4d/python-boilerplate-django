from django.conf import settings
from django.db.models import TextChoices
from rest_framework import serializers

from utils import validators
from .models import Role


# region token

class GrantTypes(TextChoices):
    PASSWORD = 'password'
    OTP = 'otp'
    REFRESH_TOKEN = 'refresh_token'


class GenerateTokensInputSerializer(serializers.Serializer):
    grant_type = serializers.ChoiceField(choices=GrantTypes.choices, required=True)
    phone = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(required=False)
    otp_code = serializers.CharField(min_length=settings.OTP_CODE_LENGTH, max_length=settings.OTP_CODE_LENGTH,
                                     required=False)
    refresh_token = serializers.CharField(required=False)
    roles = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)

    def validate_phone(self, value):
        if not validators.validate_phone(value):
            raise serializers.ValidationError({'phone': 'phone is not in a valid format'})

        return value

    def validate(self, attrs):
        super().validate(attrs)

        if attrs['grant_type'] == GrantTypes.PASSWORD:
            if not attrs['password']:
                raise serializers.ValidationError({'password': 'you should provide password field'})

        if attrs['grant_type'] == GrantTypes.OTP:
            if not attrs['otp_code']:
                raise serializers.ValidationError({'otp_code': 'you should provide otp_code field'})

        if attrs['grant_type'] == GrantTypes.REFRESH_TOKEN:
            if not attrs['refresh_token']:
                raise serializers.ValidationError({'refresh_token': 'you should provide refresh_token field'})

        return attrs


class TokensSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()
    roles = serializers.ListField(serializers.CharField())
    expires_at = serializers.IntegerField()
    # todo: user = user_serializers.UserSerializer()


# endregion

# region otp

class CreateOtpCodeInputSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, required=True)

    def validate_phone(self, value):
        if not validators.validate_phone(value):
            raise serializers.ValidationError({'phone': 'phone is not in a valid format'})

        return value


# endregion

# region role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['slug', 'name', 'permissions', ]


class CreateRoleSerializer(serializers.Serializer):
    slug = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    permissions = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=True)


class UpdateRoleSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True, default=None, required=False)
    permissions = serializers.ListField(child=serializers.CharField(), allow_empty=True, allow_null=True, default=None,
                                        required=False)

# endregion
