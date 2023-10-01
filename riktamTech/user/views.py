import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.contrib.auth.decorators import user_passes_test
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


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def create_user(request):
    if not request.method == "POST":
        return HttpResponse("Invalid request method.")
    
    # Extract user data from the POST request
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    # Create a new user
    user = CustomUser.objects.create(username=username, password=password, email=email)

    # Return a success response
    return JsonResponse({'message': 'User created successfully'})


@user_passes_test(is_admin)
def edit_user(request, user_id):

    if not request.method == "PUT":
        return HttpResponse("Invalid request method.")

    # Get the user object by user_id
    user = get_object_or_404(CustomUser, id=user_id)

    # Extract user data from the PUT request
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    # Update user fields if provided in the request
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email

    # Save the user object
    user.save()

    # Return a success response
    return JsonResponse({'message': 'User updated successfully'})
