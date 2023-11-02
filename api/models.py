from django.db import models
from endusers.models import Organization
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeStampMixIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Project(TimeStampMixIn):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class UsersInProjects(TimeStampMixIn):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class UsersInOrganizations(TimeStampMixIn):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class Team(TimeStampMixIn):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class UsersInTeams(TimeStampMixIn):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_lead = models.BooleanField(default=False)

class Announcement(TimeStampMixIn):
    title = models.CharField(max_length=128)
    body = models.CharField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
