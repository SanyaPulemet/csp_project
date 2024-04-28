"""main_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

# APPS LIBS
from storage_app import views as storage_app_views
from user_app import views as user_app_views
from user_app import urls as user_app_urls
from storage_app import urls as storage_app_urls

urlpatterns = [
    
    # USER_APP
   
    re_path(r'^admin/?', admin.site.urls, name="admin_page"),
    path('profile/', include(user_app_urls.profile_patterns)),
    path('user/<int:pk>', user_app_views.user_profile, name="user_page"),
    re_path(r'^login/?$', user_app_views.user_login, name="user_login"),
    re_path(r'^registration/?$', user_app_views.user_registration, name="registration_page"),

    # STORAGE_APP

    path('', storage_app_views.main_view, name="main_page"),
    re_path(r'^upload/?$', storage_app_views.upload_files, name="upload_files"),
    path('page/<int:page_id>', storage_app_views.page, name="page"),
    path('file/<uuid:file_id>/', include(storage_app_urls.storage_patterns)),
    path('link/<uuid:link_id>', storage_app_views.link_page, name="link_page"),

    # запасной вариант для страницы ошибок
    re_path(r'error/?$', storage_app_views.error_page, name="error_page"),

    path('pagination/', storage_app_views.pagination_pro, name='pagination_p'),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
