from django.db import models
from users.models import NetworkUser


class Post(models.Model):
    user = models.ForeignKey(NetworkUser, related_name='created_by', on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=100)
    body = models.TextField(null=False, blank=False, max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(NetworkUser, related_name='liked_by', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
