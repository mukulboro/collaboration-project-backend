from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", include("admindash.urls")),
    path("api/", include("api.urls")),
    path('dev-admin/', admin.site.urls),
]
