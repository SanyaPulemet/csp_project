from django.contrib import admin
from user_app import models as user_app_models
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(user_app_models.User, UserAdmin)
