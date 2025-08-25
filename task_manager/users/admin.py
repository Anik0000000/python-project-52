from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_superuser', 'date_joined']
    readonly_fields = ['date_joined', 'last_login']