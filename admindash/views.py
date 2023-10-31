from django.shortcuts import render, HttpResponse
from endusers.models import Organization, OrganizationAdmin
from .forms import RegisterForm

def register(request):
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

            return HttpResponse(user)

        return render(request, "register.html", {"error": form.errors.as_text})


def login(request):
    return render(request, "login.html")


def dashboard(request):
    return render(request, "dashboard.html")
