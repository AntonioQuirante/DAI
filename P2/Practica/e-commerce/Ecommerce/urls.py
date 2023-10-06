from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("etienda/", include("etienda.urls")),
    path("admin/", admin.site.urls),
]