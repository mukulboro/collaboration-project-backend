from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.ToDoView.as_view(), name="todo")
]