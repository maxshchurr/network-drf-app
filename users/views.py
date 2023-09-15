from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import NetworkUser
from .serializers import NetworkUserSerializer, NetworkUserInfoSerializer


class CreateNetworkUser(generics.CreateAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = NetworkUserSerializer

    """perform_create will be called after create method to provide user with an access token"""
    def perform_create(self, serializer):
        user = serializer.save()
        self.response_data = serializer.data

        refresh_token = RefreshToken.for_user(user)
        self.response_data['token'] = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
        }

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.response_data, status=status.HTTP_201_CREATED)


class NetworkUsersList(generics.ListAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = NetworkUserInfoSerializer


class NetworkUserInfo(generics.RetrieveAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = NetworkUserInfoSerializer
