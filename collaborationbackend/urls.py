from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", include("admindash.urls")),
    path("api/", include("api.urls")),
    path("cdn/", include("cdn.urls")),
    path("dev-admin/", admin.site.urls),
    path("users/", include("endusers.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
