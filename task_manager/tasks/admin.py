from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'author', 'executor', 'created_at']
    list_filter = ['status', 'author', 'executor', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'author']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new task
            obj.author = request.user
        super().save_model(request, obj, form, change)