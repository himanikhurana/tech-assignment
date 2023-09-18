from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Message
# Create your views here.


def sendMessage(request):
    if request.method == "POST":
        requestBody = json.loads(request.body)

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
