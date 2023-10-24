from django.urls import path, re_path, register_converter

from lyceum.catalog import converters, views

register_converter(converters.PositiveInt, "n_converter")

urlpatterns = [
    path("", views.item_list),
    path("<int:item_n>/", views.item_detail),
    re_path(r"^re/(?P<n>[1-9]\d*)/$", views.catalog_n),
    path("converter/<n_converter:n>/", views.catalog_n),
]
