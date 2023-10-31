from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_admin, name="register"),
    path("", views.login_admin, name="home"),
    path("login/", views.login_admin, name="login"),
    path("logout/", views.logout_admin, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard")
]