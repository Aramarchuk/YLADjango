from django.urls import path

from feedback import views


__all__ = ("urlpatterns",)


app_name = "feedback"

urlpatterns = [
    path("", views.feedback, name="feedback"),
]
