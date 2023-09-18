from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Group, GroupUserMap
# Create your views here.


def create(request):
    if request.method == "POST":
        requestBody = json.loads(request.body)
        newGroup = Group(groupName=requestBody['groupName'],
                         createdBy=requestBody['createdBy'], createdTime=requestBody['createdTime'])

        newGroup.save()
        currGroup = Group.objects.filter(
            groupName=requestBody['groupName'], createdBy=requestBody['createdBy'])

        groupMembers = GroupUserMap(
            associatedMembers=requestBody['members'], groupId=currGroup[0].groupId)
        groupMembers.save()

        return HttpResponse("New Group Created Successfully!")
    else:
        return HttpResponse("Invalid request method.")


def delete(request):
    if request.method == "POST":
        requestBody = json.loads(request.body)
        try:
            group = Group.objects.get(groupId=requestBody['groupId'])
        except Group.DoesNotExist:
            return HttpResponse("No Group Found!")

        if group:
            group.delete()

        return HttpResponse("Group Deleted Successfully!")
    else:
        return HttpResponse("Invalid request method.")


def getGroups(request):
    if request.method == "GET":
        availableGroups = []
        for group in Group.objects.all().values():
            availableGroups.append(group)

        return HttpResponse(json.dumps(availableGroups, cls=DjangoJSONEncoder))
    else:
        return HttpResponse("Invalid request method.")
