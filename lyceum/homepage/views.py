from django.http import HttpResponse, HttpResponseNotAllowed
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
    context = {"echo_form": EchoForm()}
    if request.method == "GET":
        return render(request, template, context)
    return HttpResponseNotAllowed(["POST"])


def echo_submit(request):
    form = EchoForm(request.POST)
    if request.method == "POST" and form.is_valid():
        return HttpResponse(
            form.cleaned_data.get("text"),
            content_type="text/plain",
            charset="utf-8",
        )
    return HttpResponseNotAllowed(["GET"])
