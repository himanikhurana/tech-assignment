from django.db import models
import uuid
# Create your models here.


class Group(models.Model):
    groupId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    groupName = models.CharField(max_length=50)
    createdBy = models.CharField(max_length=50)
    createdTime = models.DateTimeField()

    def __str__(self):
        return self.groupName


class GroupUserMap(models.Model):
    groupId = models.CharField(primary_key=True, max_length=50)
    associatedMembers = models.CharField(max_length=500)

    def __str__(self):
        return self.groupId
