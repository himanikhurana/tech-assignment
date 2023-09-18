import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
# Create your views here.


def loginRequest(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(f"You are now logged in as {username}.")
            else:
                return HttpResponse("Invalid username or password.")
        else:
            return HttpResponse("Invalid username or password.")
    else:
        return HttpResponse("Invalid request method.")


def logoutRequest(request):
    logout(request)
    return HttpResponse("You have successfully logged out.")


def getUsers(request):
    if request.method == "POST":
        availableUsers = []
        requestBody = json.loads(request.body)

        if 'conditions' in requestBody:
            for user in CustomUser.objects.filter(username=requestBody['conditions']['username'], is_superuser=0).values():
                availableUsers.append({'userName': user['username'],
                                       'firstName': user['first_name'],
                                       'lastName': user['last_name'],
                                       'email': user['email']
                                       })
        else:
            for user in CustomUser.objects.filter(is_superuser=0).values():
                availableUsers.append({'userName': user['username'],
                                       'firstName': user['first_name'],
                                       'lastName': user['last_name'],
                                       'email': user['email']
                                       })

        return HttpResponse(json.dumps(availableUsers))
    else:
        return HttpResponse("Invalid request method.")
