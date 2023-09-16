from django.contrib import admin
from .models import Post


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'created_at')


admin.site.register(Post, PostsAdmin)
