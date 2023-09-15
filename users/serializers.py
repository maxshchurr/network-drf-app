from rest_framework import serializers
from .models import NetworkUser
from rest_framework import mixins
from django.contrib.auth.hashers import make_password


class NetworkUserSerializer(serializers.ModelSerializer, mixins.CreateModelMixin):
    class Meta:
        model = NetworkUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        return NetworkUser.objects.create(**validated_data)

    def validate_password(self, value: str) -> str:
        return make_password(value)


class NetworkUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkUser
        fields = ['username', 'about_user', 'first_name', 'last_name']
