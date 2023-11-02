from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login, get_user_model
from endusers.models import Organization, OrganizationAdmin, EndUser
from api.models import Project, UsersInProjects, UsersInOrganizations, Team, UsersInTeams
from .forms import (
    RegisterForm,
    LoginForm,
    NewProjectForm,
    AddEmployeeForm,
    EmployeeToProjectForm,
    NewTeamForm,
    AddUserToTeamForm
)

User = get_user_model()


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
        users_in_organization = UsersInOrganizations.objects.filter(
            organization=organizationAdmin.organization
        )
        projects = Project.objects.filter(organization=organizationAdmin.organization)

        crop_user = users_in_organization[:5]
        crop_project = projects[:5]
        filteredData = {"projects": [], "employees": []}
        for project in crop_project:
            filteredData["projects"].append(
                {"id": project.pk, "name": project.name, "created": project.created_at}
            )

        for user in crop_user:
            filteredData["employees"].append(
                {
                    "first_name": user.user.first_name,
                    "last_name": user.user.last_name,
                    "last_login": user.user.last_login,
                    "username": user.user.username,
                }
            )

        organizationDetails = {
            "name": organizationAdmin.organization.name,
            "description": organizationAdmin.organization.description,
            "no_of_projects": organizationAdmin.organization.no_of_projects,
            "total_employees": len(users_in_organization),
            "projects": filteredData["projects"],
            "employees": filteredData["employees"],
        }
        return render(
            request, "dashboard_home.html", {"org_details": organizationDetails}
        )
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})


def dashboard_project(request):
    project_list = []
    if request.user.is_authenticated:
        error = request.GET.get("error")
        get_project = request.GET.get("get_project")
        org_admin = OrganizationAdmin.objects.get(user=request.user)
        projects = Project.objects.filter(organization=org_admin.organization)
        for project in projects:
            project_list.append(
                {"name": project.name, "created": project.created_at, "id": project.pk}
            )
        if not get_project:
            return render(
                request,
                "dashboard_project.html",
                {"projects": project_list, "error": error},
            )
        else:
            emp_list = []
            org_emp_list = []
            current_project = Project.objects.get(pk=get_project)
            employees_in_project = UsersInProjects.objects.filter(
                project=current_project
            )
            org_admin = OrganizationAdmin.objects.get(user=request.user)
            employees_in_organization = UsersInOrganizations.objects.filter(
                organization=org_admin.organization
            )
            for employee in employees_in_project:
                emp_list.append(
                    {
                        "username": employee.user.username,
                        "full_name": f"{employee.user.first_name} {employee.user.last_name}",
                        "joined": employee.created_at,
                        "id": employee.pk,
                    }
                )
            for org_emp in employees_in_organization:
                org_emp_list.append(
                    {
                        "username": org_emp.user.username,
                        "full_name": f"{org_emp.user.first_name} {org_emp.user.last_name}",
                        "id": org_emp.user.pk,
                    }
                )
            return render(
                request,
                "dashboard_project.html",
                {
                    "projects": project_list,
                    "employees": emp_list,
                    "org_employees": org_emp_list,
                    "current_project": current_project.name,
                    "current_project_id": current_project.pk,
                },
            )

    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})


def projects(request):
    if request.method == "POST":
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
            return render(
                request, "error.html", {"code": 401, "message": "Unauthorized"}
            )
    elif request.method == "GET":
        delete = request.GET.get("delete")
        if delete:
            project = Project.objects.get(pk=delete)
            print(project)
            project.delete()
            return redirect("/admin/dashboard/projects")

        else:
            return render(
                request, "error.html", {"code": 400, "message": "Bad Request"}
            )


def dashboard_employees(request):
    if request.user.is_authenticated:
        error = request.GET.get("error")
        org_admin = OrganizationAdmin.objects.get(user=request.user)
        users_in_org = UsersInOrganizations.objects.filter(
            organization=org_admin.organization
        )
        employees = []
        for employee in users_in_org:
            employees.append(
                {
                    "username": employee.user.username,
                    "email": employee.user.email,
                    "first_name": employee.user.first_name,
                    "last_name": employee.user.last_name,
                    "last_login": employee.user.last_login,
                    "joined": employee.created_at,
                }
            )
        return render(
            request,
            "dashboard_employees.html",
            {"employees": employees, "error": error},
        )
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})


def employees(request):
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = None
            try:
                user = User.objects.get(username=username, email=email)
            except:
                return redirect("/admin/dashboard/employees?error=Invalid Data")
            org_admin = OrganizationAdmin.objects.get(user=request.user)
            check_existence = UsersInOrganizations.objects.filter(
                user=user, organization=org_admin.organization
            )
            if check_existence:
                return redirect(
                    "/admin/dashboard/employees?error=User already in organization"
                )

            user_in_org = UsersInOrganizations(
                user=user, organization=org_admin.organization
            )
            user_in_org.save()
            return redirect("/admin/dashboard/employees")

        return redirect("/admin/dashboard/employees", {"error": "Invalid Input"})
    elif request.method == "GET":
        delete = request.GET.get("delete")
        if delete:
            user = User.objects.get(username=delete)
            if not user:
                return redirect("/admin/dashboard/employees?error=Error")

            user_in_org = UsersInOrganizations.objects.get(user=user)
            org_admin = OrganizationAdmin.objects.get(user=request.user)

            user_in_org.delete()
            return redirect("/admin/dashboard/employees")
        else:
            return render(
                request, "error.html", {"code": 400, "message": "Bad Request"}
            )


def employees_in_project(request):
    if request.method == "POST":
        form = EmployeeToProjectForm(request.POST)
        if form.is_valid():
            check_existence = None
            user_id = form.cleaned_data["user_id"]
            project_id = form.cleaned_data["project_id"]
            user = User.objects.get(pk=user_id)
            project = Project.objects.get(pk=project_id)

            check_existence = UsersInProjects.objects.filter(user=user, project=project)

            if check_existence:
                return redirect(
                    f"/admin/dashboard/projects?error=User Already In Project"
                )

            else:
                new_relation = UsersInProjects(user=user, project=project)
                new_relation.save()
                return redirect(f"/admin/dashboard/projects?get_project={project_id}")
        else:
            print(form.errors.as_text)
            return redirect(f"/admin/dashboard/projects?error=Select+Valid+User")
    elif request.method == "GET":
        relation_id = request.GET.get("relation")
        user_in_project = UsersInProjects.objects.get(pk=relation_id)
        project_id = user_in_project.project.pk
        user_in_project.delete()
        return redirect(f"/admin/dashboard/projects?get_project={project_id}")


def dashboard_teams(request):
    if request.user.is_authenticated:
        error = request.GET.get('error')
        org_admin = OrganizationAdmin.objects.get(user=request.user)
        projects = Project.objects.filter(organization=org_admin.organization)
        project_list = []
        team_list = []
        for project in projects:
            prj_emps = UsersInProjects.objects.filter(project=project)
            teams = Team.objects.filter(project=project)
            for team in teams:
                team_memebers = UsersInTeams.objects.filter(team=team)

                team_list.append({
                    "team_name" : team.name,
                    "team_leader" : team.leader,
                    "team_pk" : team.pk,
                    "team_members":team_memebers
                })
            project_list.append({
                "name":project.name,
                "id":project.pk,
                "users" : prj_emps,
                "teams" : team_list
            })
            team_list = []
        return render(request, "dashboard_team.html", {
            "projects":project_list,
            "error":error
        })
    else:
        return render(request, "error.html", {"code": 401, "message": "Unauthorized"})
    
def teams(request):
    if request.method == "POST":
        form = NewTeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data["team_name"]
            team_leader = form.cleaned_data["team_leader"]
            project_id = form.cleaned_data["project"]
            leader_user = User.objects.get(pk=team_leader)
            project = Project.objects.get(pk=project_id)
            new_team = Team(name=team_name, leader=leader_user, project=project)
            new_team.save()

            user_in_team = UsersInTeams(is_lead=True, user=leader_user, team=new_team)
            user_in_team.save()
            return redirect("/admin/dashboard/teams")
        else:
            return redirect(f"/admin/dashboard/teams?error={form.errors.as_text}")
        
    elif request.method == "GET":
        team_id = request.GET.get("delete")
        if team_id:
            team = Team.objects.get(pk=team_id)
            team.delete()
            return redirect("/admin/dashboard/teams")
        else:
            return redirect("/admin/dashboard/teams")
        
def users_in_teams(request):
    if request.method == "POST":
        form = AddUserToTeamForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["new_user"]
            team_id = form.cleaned_data["team"]
            user = User.objects.get(pk=user_id)
            team = Team.objects.get(pk=team_id)
            check_existence = UsersInTeams.objects.filter(user=user, team=team)
            if check_existence:
                return redirect("/admin/dashboard/teams?error=User Already in Organization")

            new_user_in_team = UsersInTeams(user=user, team=team, is_lead=False)
            new_user_in_team.save()
            return redirect("/admin/dashboard/teams")
        else:
            return redirect(f"/admin/dashboard/teams?error={form.errors.as_data}")

    elif request.method == "GET":
        user_id = request.GET.get("delete")
        team_id = request.GET.get("team")
        user = User.objects.get(pk=user_id)
        team = Team.objects.get(pk=team_id)
        user_in_team = UsersInTeams.objects.filter(user=user, team=team)
        user_in_team.delete()
        return redirect("/admin/dashboard/teams")
