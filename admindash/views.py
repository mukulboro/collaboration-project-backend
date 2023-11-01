from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from endusers.models import Organization, OrganizationAdmin
from api.models import Project
from .forms import RegisterForm, LoginForm, NewProjectForm


def register_admin(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            organization_name = data["organization_name"]
            organization_description = data["organization_description"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]

            organization = Organization(
                name=organization_name, description=organization_description
            )
            organization.save()
            saved_data = Organization.objects.get(id=organization.id)
            org_id = saved_data.id
            user = form.save()

            organization_admin = OrganizationAdmin(user=user, organization=organization)
            organization_admin.save()

            return redirect("/admin/login?newAccount=True")

        return render(request, "register.html", {"error": form.errors.as_text})


def login_admin(request):
    if request.method == "GET":
        isNew = request.GET.get("newAccount")
        if isNew:
            return render(request, "login.html", {"newAccount": isNew})
        return render(request, "login.html")
    elif request.method == "POST":
        form = LoginForm(request.POST)
        print(form.is_valid())
        if not form.is_valid():
            return render(request, "login.html", {"error": form.errors.as_text})
        else:
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, "login.html", {"error": "Invalid Credentials"})
            else:
                login(request=request, user=user)
                return redirect("/admin/dashboard")


def logout_admin(request):
    logout(request)
    return redirect("/admin/login/")


def dashboard(request):
    if request.user.is_authenticated:
        organizationAdmin = OrganizationAdmin.objects.get(user=request.user)
        organizationDetails = {
            "name": organizationAdmin.organization.name,
            "description": organizationAdmin.organization.description,
            "no_of_projects": organizationAdmin.organization.no_of_projects,
        }
        print(organizationAdmin.organization.name)
        return render(
            request, "dashboard_home.html", {"org_details": organizationDetails}
        )
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})


def dashboard_project(request):
    project_list = []
    if request.user.is_authenticated:
        org_admin = OrganizationAdmin.objects.get(user=request.user)
        projects = Project.objects.filter(organization=org_admin.organization)
        for project in projects:
            project_list.append({"name": project.name})
        print(project_list)
        return render(request, "dashboard_project.html", {"projects": project_list})
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})


def create_project(request):
    if request.user.is_authenticated:
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["prj_name"]
            org_admin = OrganizationAdmin.objects.get(user=request.user)
            org = org_admin.organization
            project = Project(name=name, organization=org)
            project.save()
            prev_proj_no = org.no_of_projects
            org.no_of_projects = prev_proj_no + 1
            org.save()
            return redirect("/admin/dashboard/projects")
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})


def dashboard_employees(request):
    if request.user.is_authenticated:
        return render(request, "dashboard_employees.html")
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})
