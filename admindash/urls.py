from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_admin, name="register"),
    path("", views.login_admin, name="home"),
    path("login/", views.login_admin, name="login"),
    path("logout/", views.logout_admin, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/projects", views.dashboard_project, name="dashboard_project"),
    path("projects/manage", views.projects, name="manage_project"),
    path("dashboard/employees", views.dashboard_employees, name="dashboard_employees"),
    path("employees/manage", views.employees, name="manage_employees"),
    path("project/employees", views.employees_in_project, name="project_employees"),
    path("dashboard/teams", views.dashboard_teams, name="dashboard_teams"),
    path("teams/manage", views.teams, name="manage_teams"),
    path("teams/employees", views.users_in_teams, name="users_in_teams"),
    path("dashboard/announcements", views.dashboard_announcements, name="dashboard_announcements"),
    path("announcement/manage", views.announcements, name="manage_announcements"),
    path("dashboard/settings", views.dashboard_account, name="dashboard_account"),
    path("dashboard/report", views.dashboard_report, name="dashboard_report"),
]