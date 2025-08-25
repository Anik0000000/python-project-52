from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password1 = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        help_text="Ваш пароль должен содержать минимум 3 символа."
    )
    password2 = forms.CharField(
        required=True,
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        help_text="Для подтверждения введите тот же пароль ещё раз."
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
                self.add_error("password2", "Пароли не совпадают.")

            if len(password1) < 3:
                self.add_error(
                    "password1",
                    "Введённый пароль слишком короткий. Он должен содержать минимум 3 символа.",
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
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password1 = forms.CharField(
        required=False,
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        help_text="Ваш пароль должен содержать минимум 3 символа."
    )
    password2 = forms.CharField(
        required=False,
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        help_text="Для подтверждения введите тот же пароль ещё раз."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username == self.instance.username:
            return username

        if User.objects.filter(username=username).exclude(
            pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Пользователь с таким именем уже существует."
            )

        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Пароли не совпадают.")

            if password1 and len(password1) < 3:
                self.add_error(
                    "password1",
                    "Введённый пароль слишком короткий. Он должен содержать минимум 3 символа.",
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


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )