from .models import NetworkUser
from datetime import datetime


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = request.user
            user.last_request_time = datetime.now()
            user.save()

        return response
