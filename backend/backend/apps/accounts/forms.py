from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserChangeForm,
                                       UserCreationForm)

UserModel = get_user_model()


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Пайдаланушы аты'}),
        label="Пайдаланушы аты"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Құпия сөз'}),
        label="Құпия сөз"
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электрондық пошта'}),
        label="Электрондық пошта"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Құпия сөз'}),
        label="Құпия сөз"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Құпия сөзді растау'}),
        label="Құпия сөзді растау"
    )
    first_name = forms.HiddenInput()
    last_name = forms.HiddenInput()
    

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пайдаланушы аты'}),
        }


class EditProfileForm(UserChangeForm):
    # username = forms.CharField(label="Username:",
    #                            max_length=32, help_text="<small id='emailHelp' class='form-text text-muted'>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(label="First Name:",
    #                              max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(label="Last Name:",
    #                             max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(label="Email",
    #                          max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(label="",
    # #                            max_length=50, widget=forms.PasswordInput(attrs={'type': 'hidden'}))

    # class Meta:
    #     model = UserModel
    #     fields = ['username', 'first_name', 'last_name',  'email']
    #     widgets = {
    #         'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пайдаланушы аты'}),
    #         'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Атыңыз'}),
    #         'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тегіңіз'}),
    #         'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электрондық пошта'}),
    #     }
    password = None  # Exclude the password field from the form

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Пайдаланушы аты',
            'email': 'Электрондық пошта',
            'first_name': 'Атыңыз',
            'last_name': 'Тегіңіз',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пайдаланушы аты'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электрондық пошта'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Атыңыз'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тегіңіз'}),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password:",
                                   max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="New password:", help_text="<small><ul class='form-text text-muted'><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul></small>",
                                    max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="New password confirmation:",
                                    max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserModel
