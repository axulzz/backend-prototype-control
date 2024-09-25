from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "curp",
            "number_phone",
            "address",
            "email",
            "photo",
            "is_active",
            "is_superuser",
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "number_phone",
        "address",
        "curp",
        "turn",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "turn",
    )
    fieldsets = (
        (
            "Informacion del usuario",
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "photo",
                    "turn",
                    "number_phone",
                    "address",
                )
            },
        ),
        (
            "Permisos",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "photo",
                    "address",
                    "curp",
                    "number_phone",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("first_name", "last_name", "email", "curp")
    ordering = ("email", "first_name", "last_name")

    filter_horizontal = (
        "groups",
        "user_permissions",
    )
