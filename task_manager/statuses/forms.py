from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if self.instance.pk:
            # For updates, exclude current instance from uniqueness check
            if Status.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_("A status with that name already exists."))
        else:
            # For creation, check if name already exists
            if Status.objects.filter(name=name).exists():
                raise forms.ValidationError(_("A status with that name already exists."))
        
        return name