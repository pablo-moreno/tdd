from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView

from config.api.v1.views import APISchema

urlpatterns = [
    path('articles/', include('blog.api.v1.urls')),
    path("schema/", APISchema.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
