from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["display_name"]

    new_password = forms.CharField(required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_pw = cleaned_data.get("new_password")
        confirm_pw = cleaned_data.get("confirm_password")
        if new_pw and new_pw != confirm_pw:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data
