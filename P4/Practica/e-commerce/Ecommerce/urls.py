from django.contrib import admin
from django.urls import include, path
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="/etienda/")),
    path("etienda/", include("etienda.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
]