from django.contrib import admin
from .models import Project


@admin.register(Project)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
        

# Register your models here.

