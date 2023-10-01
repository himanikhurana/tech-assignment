from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginRequest),
    path('logout', views.logoutRequest),
    path('getUsers', views.getUsers),
    path('createUser', views.create_user),
    path('editUserDetails', views.edit_user)
]
