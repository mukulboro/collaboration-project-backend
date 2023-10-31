from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cdn.models import ProfilePicture

ROLE_CHOICES = (("ADMIN", "ADMIN"), ("USER", "USER"))
class TimeStampMixIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

class Organization(TimeStampMixIn):
    name = models.CharField(max_length=128)
    description = models.TextField()
    no_of_projects = models.IntegerField(default=0)

class OrganizationAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)

class EndUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ForeignKey(ProfilePicture, on_delete=models.DO_NOTHING)


# Create your models here.
