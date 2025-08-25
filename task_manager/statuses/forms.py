from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )

    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if self.instance.pk:
            # For updates, exclude current instance from uniqueness check
            if Status.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Статус с таким именем уже существует.")
        else:
            # For creation, check if name already exists
            if Status.objects.filter(name=name).exists():
                raise forms.ValidationError("Статус с таким именем уже существует.")
        
        return name