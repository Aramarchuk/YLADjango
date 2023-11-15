from datetime import timedelta

from django.conf import settings
from django.contrib import messages
import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone

import users.forms
import users.models

__all__ = "signup"


def signup(request):
    template = "users/signup.html"
    signup_form = users.forms.SignupForm(
        request.POST or None,
    )
    context = {
        "signup_form": signup_form,
    }
    if request.method == "POST" and signup_form.is_valid():
        user = signup_form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        users.models.Profile.objects.create(user=user)
        mail_to = signup_form.cleaned_data.get("email", "example@gmail.com")
        activate_link = request.build_absolute_uri(
            reverse("users:activate", kwargs={"username": user.username}),
        )
        send_mail(
            "Активация пользователя",
            f"для активации перейдите по ссылке \n {activate_link}",
            settings.DJANGO_MAIL,
            [mail_to],
            fail_silently=False,
        )
        messages.success(
            request,
            "Регистрация успешна!",
        )
        messages.success(
            request,
            "Письмо для активации отправлено!",
        )

        return redirect("users:signup")

    return render(request, template, context)


def activate_user(request, username):
    user = django.contrib.auth.models.User.objects.get(
        username=username,
    )
    if timezone.now() - timedelta(hours=12) <= user.date_joined:
        user.is_active = True
        user.save()
        new_user = django.contrib.auth.models.User.objects.get(
            username=username,
        )
        print(new_user.is_active)
        return redirect("users:login")

    return HttpResponseNotFound(
        "Пользователь не найден или время активации истекло",
    )


def user_list(request):
    template = "users/user_list.html"
    users_list = list(
        django.contrib.auth.models.User.objects.filter(is_active=True),
    )
    context = {
        "users_list": users_list,
    }
    return render(request, template, context)


def user_deatil(request):
    template = "users/user_detail.html"
    user = get_object_or_404(
        django.contrib.auth.models.User,
        id=request.user.id,
    )
    profile = user.profile
    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, template, context)


@login_required
def profile(request):
    template = "users/profile.html"
    user = get_object_or_404(
        django.contrib.auth.models.User,
        id=request.user.id,
    )
    profile_form = users.forms.ProfileChangeForm(
        request.POST or None,
        request.FILES or None,
        instance=user.profile,
    )
    user_form = users.forms.UserChangeForm(
        request.POST or None,
        instance=user,
    )
    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                "Изменения успешны!",
            )
            return redirect("users:profile")
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, template, context)
