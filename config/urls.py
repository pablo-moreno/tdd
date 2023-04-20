from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("config.api.v1.urls")),
    path("watchman", include("watchman.urls")),
]
