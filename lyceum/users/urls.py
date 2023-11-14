import django.contrib.auth.views
from django.urls import path

import users.views


app_name = "users"

urlpatterns = [
    path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    path(
        "logged_out/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="users/logged_out.html",
        ),
        name="logout",
    ),
    path(
        "password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change_done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "signup/",
        users.views.signup,
        name="signup",
    ),
    path(
        "activate/<str:username>",
        users.views.activate_user,
        name="activate",
    ),
    path(
        "user_list/",
        users.views.user_list,
        name="user_list",
    ),
    path(
        "user_detail/",
        users.views.user_deatil,
        name="user_detail",
    ),
    path(
        "profile/",
        users.views.profile,
        name="profile",
    ),
]
