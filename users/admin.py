from django.contrib import admin
from .models import NetworkUser


class NetworkUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


admin.site.register(NetworkUser, NetworkUserAdmin)
