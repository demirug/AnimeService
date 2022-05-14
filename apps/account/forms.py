from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.account.models import User


class UserCreationForm(forms.ModelForm):
    """Form for user registration"""
    username = forms.CharField(label=_("Username"), widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={"class": "form-control"}))

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={"class": "form-control"}))

    password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput(
        attrs={"class": "form-control"}
    ))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean(self, *args, **kwargs):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))

        if len(password2) < 8:
            raise ValidationError(_("Minimum password length 8 chars"))

        if password2 == email or password2 == username:
            raise ValidationError(_("Password can't be as email or nickname"))

        user = User.objects.filter(username=username).first()

        if user is not None:
            if not user.is_active:
                raise ValidationError(
                    _("User already registered. Verify your account with the code sent to your email"))
            raise ValidationError(_("User with that nickname already exists"))

        return super().clean(*args, **kwargs)

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')