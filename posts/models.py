from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

from users.models import NetworkUser


class PostManager(models.Manager):
    def likes_analytics(self, date_from, date_to):
        return (
            self.filter(created_at__range=(date_from, date_to))
            .values('created_at')
            .annotate(likes_count=Count('liked_by'))

            # self.filter(created_at__range=(date_from, date_to))
            # .annotate(date=TruncDate('created_at'))
            # .values('date')
            # .annotate(likes_count=Count('liked_by'))

        )



class Post(models.Model):
    user = models.ForeignKey(NetworkUser, related_name='created_by', on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=100)
    body = models.TextField(null=False, blank=False, max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(NetworkUser, related_name='liked_by', null=True, blank=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
