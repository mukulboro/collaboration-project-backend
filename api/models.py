from django.db import models
from endusers.models import Organization
from django.contrib.auth import get_user_model

User = get_user_model()

TODO_STATUS_CHOICES = (
    ("TODO", "TODO"),
    ("PROGRESS", "PROGRESS"),
    ("COMPLETE", "COMPLETE"),
)

TODO_PRIORITY_CHOCICES = (
    ("HIGH", "HIGH"),
    ("LOW", "LOW"),
    ("MEDIUM", "MEDIUM")
)

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


class Todo(TimeStampMixIn):
    title = models.CharField(max_length=128)
    body = models.CharField()
    status = models.CharField(choices=TODO_STATUS_CHOICES)
    priority = models.CharField(choices=TODO_PRIORITY_CHOCICES)
    assigned_to = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
