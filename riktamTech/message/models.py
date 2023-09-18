from django.db import models
import uuid
# Create your models here.


class Message(models.Model):
    messageId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=50)
    groupId = models.CharField(max_length=50)
    sentBy = models.CharField(max_length=500)
    sentTime = models.DateTimeField(max_length=50)
    likes = models.IntegerField()
    likedBy = models.CharField(max_length=5000)

    def __str__(self):
        return self.message
