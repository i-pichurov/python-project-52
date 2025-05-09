from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password2')
        if len(password) < 3:
            raise ValidationError(_('Пароль слишком короткий. Он должен содержать не менее 3 символов.'))
        return password


class CustomUserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput,
        required=False,
        help_text="Пароль должен содержать минимум 3 символа."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Пароли не совпадают.")
            if len(password1) < 3:
                self.add_error("password2", "Пароль должен быть не менее 3 символов.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user