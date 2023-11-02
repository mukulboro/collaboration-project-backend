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
    path("project/employees", views.employees_in_project, name="project_employees")
]