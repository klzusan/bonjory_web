from django.urls import path
from . import views

urlpatterns = [
    path('', views.verPost_list, name='verPost_list'),
    path('post/<int:pk>/', views.verPost_detail, name='verPost_detail'),
    path('post/new/', views.verPost_new, name='verPost_new'),
    path('post/<int:pk>/edit/', views.verPost_edit, name='verPost_edit'),
    path('drafts/', views.verPost_draft_list, name='verPost_draft_list'),
]