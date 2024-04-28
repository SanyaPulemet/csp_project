from django.urls import path, re_path
from storage_app import views

storage_patterns = [
    path('', views.file_page, name="file_page"),
    re_path(r'delete/?$', views.delete_file, name="delete"),
]