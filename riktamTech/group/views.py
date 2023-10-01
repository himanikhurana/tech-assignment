from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Group, GroupUserMap
from ..user.models import *
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


def add_member_to_group(request):
    if not request.method == "POST":
        return HttpResponse("Invalid request method.")
    
    requestBody = json.loads(request.body)
    # Get the group based on group_id
    group = get_object_or_404(Group, id=requestBody['groupId'])

    # Check if the user making the request is an admin of the group
    if request.user not in group.admins.all():
        return JsonResponse({'error': 'You are not an admin of this group.'}, status=403)

    # Get the user to be added based on user_id
    user_to_add = get_object_or_404(CustomUser, id=requestBody['userId'])

    # Add the user to the group's members
    group.members.add(user_to_add)
    
    #update group user map
    exisitng_user_map = GroupUserMap.objects.get(groupId=requestBody['groupId'])
    exisitng_user_map.associatedMembers = exisitng_user_map.associatedMembers + requestBody['userId']
    exisitng_user_map.save()

    # Return a success response
    return JsonResponse({'success': 'User added to the group.'})


def remove_member_from_group(request):
    if not request.method == "POST":
        return HttpResponse("Invalid request method.")

    requestBody = json.loads(request.body)

    # Get the group based on group_id
    group = get_object_or_404(Group, id=requestBody['groupId'])

    # Check if the user making the request is an admin of the group
    if request.user not in group.admins.all():
        return JsonResponse({'error': 'You are not an admin of this group.'}, status=403)

    # Get the user to be removed based on user_id
    user_to_remove = get_object_or_404(CustomUser, id=requestBody['userId'])

    # Remove the user from the group's members
    group.members.remove(user_to_remove)

    #update group user map
    exisitng_user_map = GroupUserMap.objects.get(groupId=requestBody['groupId'])
    exisitng_user_map.associatedMembers = exisitng_user_map.associatedMembers.replace(requestBody['userId'], '')
    exisitng_user_map.save()

    # Return a success response
    return JsonResponse({'success': 'User removed from the group.'})


