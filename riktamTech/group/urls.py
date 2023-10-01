from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create),
    path('delete', views.delete),
    path('getGroups', views.getGroups),
    path('addMember', views.add_member_to_group),
    path('deleteMember', views.remove_member_from_group)
]
