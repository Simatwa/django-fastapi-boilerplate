from django import forms
from django.contrib.auth.hashers import make_password

from users.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "username",
            "address",
            "phone_number",
            "email",
            "password",
            # "profile",
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            return make_password(password)
        return password


class CustomUserUpdateForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            # "gender",
            # "username",
            "phone_number",
            "email",
            "address",
            "password",
            # "profile",
        ]
