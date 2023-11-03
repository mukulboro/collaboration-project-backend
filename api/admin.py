from django.contrib import admin
from .models import (
    Project,
    UsersInOrganizations,
    UsersInProjects,
    Team,
    UsersInTeams,
    Announcement,
    Todo,
)


@admin.register(
    Project,
    UsersInOrganizations,
    UsersInProjects,
    Team,
    UsersInTeams,
    Announcement,
    Todo,
)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


# Register your models here.
