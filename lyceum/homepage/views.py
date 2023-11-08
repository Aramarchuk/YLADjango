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
    if request.method == "GET":
        template = "homepage/echo.html"
        context = {"form": EchoForm()}
        return render(request, template, context)
    return HttpResponseNotAllowed(["POST"])


def echo_submit(request):
    if request.method == "POST":
        form = EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return HttpResponse(
                text,
                content_type="text/plain charset=UTF-8",
            )
    return HttpResponseNotAllowed(["POST"])
