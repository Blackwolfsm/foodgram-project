from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_filter = ('username', 'email')
