from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'is_active')}),
        ('Personal info', {'fields': ('avatar', 'last_login')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email',)
    ordering = ()
    filter_horizontal = ()


admin.site.unregister(Group)