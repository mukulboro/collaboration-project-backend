from django.urls import path
from . import views

urlpatterns = [
    path("project-media/", views.ProjectMediaView.as_view(), name="project-media"),
    path("documents/", views.DocumentView.as_view(), name="documents")
]