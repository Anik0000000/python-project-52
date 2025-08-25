import django_filters
from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        field_name='status',
        lookup_expr='exact',
        empty_label='Статус',
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='executor',
        lookup_expr='exact',
        empty_label='Исполнитель',
        label='Исполнитель',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        lookup_expr='exact',
        empty_label='Метка',
        label='Метка',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']