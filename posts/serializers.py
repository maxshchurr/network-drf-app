from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
