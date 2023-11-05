from django.db import models
from endusers.models import Organization
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
import uuid

User = get_user_model()

TODO_STATUS_CHOICES = (
    ("TODO", "TODO"),
    ("PROGRESS", "PROGRESS"),
    ("COMPLETE", "COMPLETE"),
)

TODO_PRIORITY_CHOCICES = (("HIGH", "HIGH"), ("LOW", "LOW"), ("MEDIUM", "MEDIUM"))


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
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class ProjectMedia(TimeStampMixIn):
    def image_name(instance, filename):
        ext = filename.split(".")[-1]
        filename = "{}.{}".format(uuid.uuid4().hex, ext)
        return os.path.join("media/project/", filename)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_name)
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
