from django.urls import path

from lyceum.homepage import views


urlpatterns = [
    path("", views.home),
    path("coffee/", views.coffee),
]
