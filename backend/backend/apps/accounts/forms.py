from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserChangeForm,
                                       UserCreationForm)

UserModel = get_user_model()


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        label="Имя пользователя"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label="Пароль"
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
        label="Электронная почта"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        label="Подтвердите пароль"
    )
    first_name = forms.HiddenInput()
    last_name = forms.HiddenInput()

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }


class EditProfileForm(UserChangeForm):
    password = None  # Исключить поле пароля из формы

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'first_name': 'Ваше имя',
            'last_name': 'Ваша фамилия',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль:",
                                   max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="Новый пароль:", help_text="<small><ul class='form-text text-muted'><li>Ваш пароль не должен быть слишком похож на вашу личную информацию.</li><li>Ваш пароль должен содержать не менее 8 символов.</li><li>Ваш пароль не должен быть общепринятым паролем.</li><li>Ваш пароль не должен быть полностью числовым.</li></ul></small>",
                                    max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Подтверждение нового пароля:",
                                    max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserModel
