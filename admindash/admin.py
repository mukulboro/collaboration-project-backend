from collections.abc import Sequence
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Organization, OrganizationAdmin


@admin.register(Organization, OrganizationAdmin)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request: HttpRequest) -> Sequence[str]:
        return [field.name for field in self.model._meta.concrete_fields]
        