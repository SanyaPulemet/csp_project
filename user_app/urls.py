from django.urls import path, re_path
from user_app import views

profile_patterns = [
    path('', views.user_profile, name="user_profile"),
    re_path(r'logout/?$', views.user_logout, name="user_logout"),
    re_path(r'change_data/?$', views.user_data_change, name="user_data_change_func"),
    re_path(r'change_password/?$', views.user_password_change, name="user_password_change_func"),
    path(r'delete/?$', views.user_delete, name="user_delete")
]