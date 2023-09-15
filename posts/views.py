from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostCreateSerializer, PostListSerializer


class CreatePost(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostInfo(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostListSerializer







