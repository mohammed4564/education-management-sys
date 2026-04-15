from rest_framework import serializers
from .models import UserInfo
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return UserInfo.objects.create(**validated_data)