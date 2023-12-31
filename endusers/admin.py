from django.contrib import admin
from .models import CustomUser, Organization, OrganizationAdmin, EndUser


@admin.register(CustomUser, Organization, OrganizationAdmin, EndUser)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
        

# Register your models here.
