from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        required=True,
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Your password must contain at least 3 characters.")
    )
    password2 = forms.CharField(
        required=True,
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Enter the same password again for verification.")
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", _("Passwords do not match."))

            if len(password1) < 3:
                self.add_error(
                    "password1",
                    _("The entered password is too short. It must contain at least 3 characters."),
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserRegistrationForm(UserCreateForm):
    pass


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username == self.instance.username:
            return username

        if User.objects.filter(username=username).exclude(
            pk=self.instance.pk).exists():
            raise forms.ValidationError(
                _("A user with that username already exists.")
            )

        return username


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )