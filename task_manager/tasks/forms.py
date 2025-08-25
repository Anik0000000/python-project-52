from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        label=_('Description'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Labels'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure empty option for executor
        self.fields['executor'].empty_label = _('--------')