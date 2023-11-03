from django.urls import path
from . import views

urlpatterns = [
    path("profile-picture/", views.ProfilePictureView.as_view(), name="profile-picture")
]