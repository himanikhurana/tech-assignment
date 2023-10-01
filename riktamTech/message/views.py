from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Message
from ..group.models import Group
# Create your views here.


def sendMessage(request):
    if request.method == "POST":
        requestBody = json.loads(request.body)

        # Get the group based on the group_id
        group = get_object_or_404(Group, id=requestBody['groupId'])

        # Check if the user is a member of the group
        if request.user not in group.members.all():
            return JsonResponse({'error': 'You are not a member of this group.'}, status=403)

        newMessage = Message(message=requestBody['message'],
                                groupId=requestBody['groupId'],
                                sentBy=requestBody['sentBy'],
                                sentTime=requestBody['sentTime'],
                                likes=0,
                                likedBy="")

        newMessage.save()

        return HttpResponse("Message Sent Successfully!")
    else:
        return HttpResponse("Invalid request method.")


def likeMessage(request):
    if request.method == "POST":
        requestBody = json.loads(request.body)
        message = Message.objects.filter(
            messageId=requestBody['messageId']).values()

        if message[0]['likedBy'] == "":
            message.update(likedBy=requestBody['user'], likes=1)
        else:
            likedBy = set(message[0]['likedBy'].split(','))
            likedBy.add(requestBody['username'])
            message.update(likedBy=",".join(likedBy), likes=len(likedBy))

        return HttpResponse("Message Liked Successfully!")
    else:
        return HttpResponse("Invalid request method.")


def getMessage(request):
    if request.method == "POST":
        messages = []
        requestBody = json.loads(request.body)

        if 'conditions' in requestBody:
            for group in Message.objects.filter(groupId=requestBody['conditions']['groupId']).values():
                messages.append(group)
        else:
            for group in Message.objects.all().values():
                messages.append(group)

        return HttpResponse(json.dumps(messages, cls=DjangoJSONEncoder))
    else:
        return HttpResponse("Invalid request method.")
