from django.urls import path, re_path, register_converter

from catalog import converters, views

register_converter(converters.PositiveInt, "n_converter")

app_name = "catalog"
urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:item_n>/", views.item_detail, name="item_detail"),
    re_path(r"^re/(?P<n>[1-9]\d*)/$", views.catalog_n),
    path("converter/<n_converter:n>/", views.catalog_n),
]
