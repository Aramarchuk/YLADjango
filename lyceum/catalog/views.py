from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def item_list(request):
    template = "catalog/catalog.html"
    context = {"items": list(Item.objects.all())}
    print(context)
    return render(request, template, context)


def item_detail(request, item_n):
    return HttpResponse("<body>Подробно элемент</body>")


def catalog_n(request, n):
    return HttpResponse(n)
