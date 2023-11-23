from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.ToDoView.as_view(), name="todo"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("team-members/", views.TeamMembersView.as_view(), name="team_members")
]