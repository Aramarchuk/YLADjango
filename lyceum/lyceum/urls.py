"""
URL configuration for lyceum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
import django.conf
import django.conf.urls.static
from django.contrib import admin
import django.contrib.auth.urls
import django.contrib.staticfiles.urls
import django.urls
from django.urls import include, path


if django.conf.settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("feedback/", include("feedback.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include(django.contrib.auth.urls)),
]

if django.conf.settings.DEBUG:
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    if django.conf.settings.MEDIA_ROOT:
        urlpatterns += django.conf.urls.static.static(
            django.conf.settings.MEDIA_URL,
            document_root=django.conf.settings.MEDIA_ROOT,
        )
    urlpatterns += django.contrib.staticfiles.urls.staticfiles_urlpatterns()
urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)
