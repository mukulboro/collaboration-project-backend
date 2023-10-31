from django.db import models

class TimeStampMixIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Organization(TimeStampMixIn):
    name = models.CharField(max_length=128)
    description = models.TextField()
    no_of_projects = models.IntegerField(default=0)

class OrganizationAdmin(TimeStampMixIn):
    email = models.EmailField()
    password = models.CharField()
    username = models.CharField(max_length=64)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
