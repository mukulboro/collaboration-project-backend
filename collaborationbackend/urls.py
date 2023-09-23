from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", include("admin.urls")),
    path('dev-admin/', admin.site.urls),
]
