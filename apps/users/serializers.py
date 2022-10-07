from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'is_active', 'role', 'date_joined',
        ]


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'role', 'is_active']


class UpdateProfileSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'old_password', 'new_password']


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['old_password', 'new_password']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, value):
        data = super(CustomTokenObtainPairSerializer, self).validate(value)
        data['user'] = GetUserSerializer(self.user).data
        return data
