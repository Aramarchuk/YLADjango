from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
from homepage.forms import EchoForm


__all__ = ()


def home(request):
    template = "homepage/home.html"
    context = {
        "items": catalog.models.Item.objects.on_main(),
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=418)


def echo(request):
    template = "homepage/echo.html"
    context = {}
    return render(request, template, context)


def echo_submit(request):
    form = EchoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return HttpResponse(form.cleaned_data.get("text"))
