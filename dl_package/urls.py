from django.urls import path
from . import views

urlpatterns = [
    path('', views.verPost_list, name='verPost_list'),
]