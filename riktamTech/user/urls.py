from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginRequest),
    path('logout', views.logoutRequest),
    path('getUsers', views.getUsers),
]
