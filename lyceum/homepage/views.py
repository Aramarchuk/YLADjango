from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


__all__ = ()


def home(request):
    template = "homepage/home.html"
    context = {
        "items": catalog.models.Item.objects.on_main(),
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=418)
