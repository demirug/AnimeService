from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _, get_language
from apps.account.models import User, AccountSettings
from shared.mixins.translate import TranslateFormWidgetMixin
from shared.services.email import send_email
from shared.services.translation import get_field_data_by_lang


class AccountSettingsForm(TranslateFormWidgetMixin, forms.ModelForm):

    def get_widgets(self) -> dict:
        return {"change_email": CKEditorUploadingWidget(),
                "registered_email": CKEditorUploadingWidget(),
                "reset_email": CKEditorUploadingWidget()
                }

    class Meta:
        model = AccountSettings
        fields = "__all__"


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

        config = AccountSettings.get_solo()

        if len(password2) < config.min_password_len:
            raise ValidationError(_("Minimum password length %s chars") % config.min_password_len)

        if len(password2) > config.max_password_len:
            raise ValidationError(_("Maximum password length %s chars") % config.max_password_len)

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


class AccountUpdateForm(forms.ModelForm):
    """Form for changing user data"""
    avatar = forms.ImageField(label=False, required=False, widget=forms.FileInput(attrs={"style": "display: none;"}))
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        _email = self.cleaned_data['email']

        if 'email' not in self.changed_data:
            return _email

        if User.objects.filter(email=_email).exists():
            raise ValidationError(_("User with that email already exists"))

        self._send_validation_token(_email)

        return self.user.email

    def _send_validation_token(self, email):

        # Generate user email token
        _token = salted_hmac(
            self.user.pk,
            f"{self.user.email}{email}",
            secret=settings.SECRET_KEY,
            algorithm='sha1'
        ).hexdigest()[::2]

        url = '{domain}{path}'.format(domain=Site.objects.get_current().domain,
                                      path=reverse("account:change_email", kwargs={"email": email, "token": _token}))

        obj: AccountSettings = AccountSettings.get_solo()
        title = get_field_data_by_lang(obj, get_language(), "change_email_title")
        context = get_field_data_by_lang(obj, get_language(), "change_email").format(url=url)

        send_email(email, title, context)

    class Meta:
        model = User
        fields = ('avatar', 'email')


class UserPasswordChangeForm(forms.Form):
    """Form for user password change"""

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean_old_password(self):
        """Validate old password"""
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(_("Incorrect old password"))
        return old_password

    def clean_new_password2(self):
        """Validate new password"""
        new_password1 = self.cleaned_data["new_password1"]
        new_password2 = self.cleaned_data["new_password2"]

        if new_password2 != new_password1:
            raise ValidationError(_("Passwords not match"))

        config = AccountSettings.get_solo()

        if len(new_password2) < config.min_password_len:
            raise ValidationError(_("Minimum password length %s chars") % config.min_password_len)

        if len(new_password2) > config.max_password_len:
            raise ValidationError(_("Maximum password length %s chars") % config.max_password_len)

        return new_password2

    def save(self, commit=True):
        """Set new password for user"""
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class AccountResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))


class AccountResetConfirmForm(forms.Form):
    """Form for user registration"""
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={"class": "form-control"}))

    password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput(
        attrs={"class": "form-control"}
    ))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))

        config = AccountSettings.get_solo()

        if len(password2) < config.min_password_len:
            raise ValidationError(_("Minimum password length %s chars") % config.min_password_len)

        if len(password2) > config.max_password_len:
            raise ValidationError(_("Maximum password length %s chars") % config.min_password_len)

        if password2 == self.user.email or password2 == self.user.username:
            raise ValidationError(_("Password can't be as email or username"))

        return super().clean(*args, **kwargs)


class AccountLoginForm(forms.Form):
    username = forms.CharField(label="",
                            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Login")}))

    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control",
               "placeholder": _("Password")}
    ))

    remember_me = forms.BooleanField(label="", required=False,
                                     widget=forms.CheckboxInput(attrs={"class": "form-check-input", "checked": ""}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self, *args, **kwargs):

        login = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = User.objects.filter(username=login).first()

        if not user or not user.check_password(password):
            raise ValidationError(_("Incorrect login or password"))

        if not user.is_active:
            raise ValidationError(_("Account not active. Please verify email"))

        self.user = user

        return super().clean(*args, **kwargs)

    def get_user(self):
        return self.user
