from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create),
    path('delete', views.delete),
    path('addMember/', views.create),
    path('getGroups', views.getGroups)
]
