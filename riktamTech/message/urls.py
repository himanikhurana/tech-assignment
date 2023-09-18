from django.urls import path
from . import views

urlpatterns = [
    path('sendMessage', views.sendMessage),
    path('likeMessage', views.likeMessage),
    path('getMessage', views.getMessage),
]
