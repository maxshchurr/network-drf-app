from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from datetime import datetime

from .models import NetworkUser
from .serializers import NetworkUserSerializer, NetworkUserInfoSerializer


class CreateNetworkUser(generics.CreateAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = NetworkUserSerializer

    """perform_create will be called after create method to provide user with an access token"""
    def perform_create(self, serializer):
        user = serializer.save()
        user.last_login = datetime.now()
        user_group = Group.objects.get(name='networkusers')
        user.groups.add(user_group)
        user.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)


class NetworkUsersList(generics.ListAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = NetworkUserInfoSerializer


class NetworkUserInfo(generics.RetrieveAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = NetworkUserInfoSerializer


class NetworkUserActivity(APIView):
    def get(self, request):
        user = request.user

        if user.is_authenticated:
            login_time = user.last_login
            last_request_time = user.last_request_time

            response_data = {
                'login_time': login_time,
                'last_request_time': last_request_time,
                }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

