from django.contrib import admin

from .models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']