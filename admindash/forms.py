from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    organization_name = forms.CharField(max_length=255)
    organization_description = forms.CharField()
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    username = forms.CharField(max_length=64)
    password1 = forms.CharField()
    password2 = forms.CharField()
    role = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "first_name", "last_name")
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField()

class NewProjectForm(forms.Form):
    prj_name = forms.CharField(max_length=128)

class AddEmployeeForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.CharField(max_length=128)

class EmployeeToProjectForm(forms.Form):
    user_id = forms.IntegerField()
    project_id = forms.IntegerField()

class NewTeamForm(forms.Form):
    team_name = forms.CharField(max_length=64)
    team_leader = forms.IntegerField()
    project = forms.IntegerField()

class AddUserToTeamForm(forms.Form):
    new_user = forms.IntegerField()
    team = forms.IntegerField()

class NewAnnouncementForm(forms.Form):
    title = forms.CharField(max_length=128)
    body = forms.CharField()
    project = forms.IntegerField()

class SettingsForm(forms.Form):
    org_name = forms.CharField(max_length=128)
    org_description = forms.CharField()
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email_address = forms.EmailField()
    password1 = forms.CharField(max_length=64, required=False)
    password2 = forms.CharField(max_length=64, required=False)


