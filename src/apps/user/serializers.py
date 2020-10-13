from rest_framework import serializers

from utils import validators
from .models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['phone', 'is_admin', 'is_active', 'profile', ]


class CreateUserInputSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(required=True)
    is_admin = serializers.BooleanField(default=False, required=False)
    is_active = serializers.BooleanField(default=True, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    roles = serializers.ListField(child=serializers.CharField(), allow_empty=True, default=[], required=False)

    def validate_phone(self, value):
        if not validators.validate_phone(value):
            raise serializers.ValidationError({'phone': 'phone is not in a valid format'})

        return value


class UpdateUserInputSerializer(serializers.Serializer):
    is_admin = serializers.BooleanField(default=None, allow_null=True, required=False)
    is_active = serializers.BooleanField(default=None, allow_null=True, required=False)
    first_name = serializers.CharField(max_length=30, allow_null=True, default=None, required=False)
    last_name = serializers.CharField(max_length=30, allow_null=True, default=None, required=False)
    roles = serializers.ListField(child=serializers.CharField(), allow_empty=True, allow_null=True, default=None,
                                  required=False)
