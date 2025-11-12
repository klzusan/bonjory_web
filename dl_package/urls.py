from django.urls import path
from . import views

urlpatterns = [
    # path('', views.verPost_list, name='verPost_list'),
    path('', views.matsu_fes, name='matsu_fes'),
    path('post/<int:pk>/', views.verPost_detail, name='verPost_detail'),
    path('post/new/', views.verPost_new, name='verPost_new'),
    path('post/<int:pk>/edit/', views.verPost_edit, name='verPost_edit'),
    path('drafts/', views.verPost_draft_list, name='verPost_draft_list'),
    path('post/<int:pk>/remove/', views.verPost_remove, name='post_remove'),
    path('post/<int:pk>/publish/', views.verPost_publish, name='verPost_publish'),
    path('download/', views.download_file, name="download_file"),
    path('upload/', views.zip_upload, name="zip_upload"),
]