from django.db import models
from django.contrib.auth.models import AbstractUser


class NetworkUser(AbstractUser):
    about_user = models.CharField(max_length=100, blank=True)
    last_request_time = models.DateTimeField(null=True, blank=True)
