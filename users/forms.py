from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError

from users.tasks import send_verification_email

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите имя пользователя или email", }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите пароль", }))

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("username", "password")

    def confirm_login_allowed(self, user):
        if not user.is_verified_email and not user.is_superuser:
            message = "Email не верефицирован!"
            raise ValidationError(
                message=message,
                code='not_verified_email',
            )
        return super(UserLoginForm, self).confirm_login_allowed(user)


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите имя", }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите Фамилию", }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите имя пользователя", }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите email", }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4", "placeholder": "Введите пароль", }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4", "placeholder": "Подтвердите пароль", }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=True)
        send_verification_email.delay(user.pk)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "custom-file-input"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control py-4", "readonly": True}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", "username", "email",)
