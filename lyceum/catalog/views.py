from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item


__all__ = ()


def item_list(request):
    template = "catalog/catalog.html"
    context = {"items": Item.objects.published().order_by("category__name")}
    return render(request, template, context)


def item_detail(request, item_n):
    template = "catalog/detail.html"
    item = get_object_or_404(
        Item.objects.published(),
        pk=item_n,
    )
    context = {"item": item}
    return render(request, template, context)


def catalog_n(request, n):
    return HttpResponse(n)
