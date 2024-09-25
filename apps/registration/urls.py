# The views used below are normally mapped in the AdminSite instance.
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

import os

from django.contrib.auth import views
from django.urls import path
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.conf import settings
from .views import index

app_name = "registration"



def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    return HttpResponseRedirect(os.environ.get("NEXT_PUBLIC_URL", "") + '/auth/signout')  # Redirigir a Next.js

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("", index, name="auth_index"),
]
