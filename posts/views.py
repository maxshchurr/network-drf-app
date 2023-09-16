from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime


from posts.models import Post
from posts.serializers import PostCreateSerializer, PostListSerializer


class CreatePost(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostList(generics.ListAPIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostInfo(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostLike(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user not in instance.liked_by.all():
            instance.liked_by.add(user)
        else:
            instance.liked_by.remove(user)

        instance.save()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikesAnalyticsView(APIView):
    def get(self, request):
        date_from_str = self.request.query_params.get('date_from')
        date_to_str = self.request.query_params.get('date_to')

        if not date_from_str or not date_to_str:
            return JsonResponse(
                {'error message': 'Both date_from and date_to parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            datetime.strptime(date_from_str, '%Y-%m-%d').date()
            datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse(
                {'error message': 'Invalid date format. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if date_from_str > date_to_str:
            return JsonResponse(
                {'error message': 'Date_from must be less than date_to.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        analytics_data = Post.objects.likes_analytics(date_from_str, date_to_str)
        print(analytics_data)

        if analytics_data:
            return JsonResponse(
                list(analytics_data), safe=False)

        return JsonResponse({'message': 'No likes for such period!'})
