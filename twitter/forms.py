from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255, label='Wprowadź hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255, label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        query_set = User.objects.filter(email=email)
        if query_set.exists():
            raise forms.ValidationError('E-mail jest już zajęty')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są takie same")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255, label='Wprowadź hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255, label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są takie same")
        return password2

    def save(self, commit=True):
        user = super(UserAdminForm).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'active', 'admin']

    def clean_password(self):
        return self.initial['password']


class AuthenticationFormExtended(AuthenticationForm):
    password = forms.CharField(
        label='Hasło',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': 'Proszę wprowadzić poprawny %(username)s i hasło. Proszę zwrócić uwagę na wielkość liter.'
    }


