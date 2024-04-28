from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from user_app.forms import *
from user_app import models as user_models
from storage_app import models as storage_models
from datetime import datetime
from django.views.decorators.cache import cache_page

# Create your views here.

# COMPLETE
@cache_page(1)
def user_registration(request):

    # Если пользователь авторизован, то перенаправить на профиль
    if request.user.is_authenticated:
        return redirect('/profile')

    # Если данные формы валидны, то 
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile')
        else:
            return render(request, "registration.html", {"form": form})
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration.html", {"form": form})

@cache_page(1)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile/')
    
    if request.method == 'POST':
        form = UserLogin(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/profile/')
        else:
            return render(request, 'login.html', {'form': form, 'error_message': "Данные неверны!"})
            
    elif request.method == "GET":
        form = UserLogin()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/login')

def user_data_change(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user_form = CustomUserDataChangeForm(request.POST, request.FILES, instance=request.user)
            tag_form = TagForm(request.POST)

            if user_form.is_valid() and tag_form.is_valid():
                user = user_form.save()
                unredacted_Tag = tag_form.cleaned_data['tag_field']
                unredacted_Tag.replace(' ', '')
                tags = unredacted_Tag.split(',')
                for tag in tags:
                    tag_obj = user_models.UserTag()
                    tag_obj.text = tag
                    tag_connection = user_models.UserTagConnectionTable()
                    tag_connection.user_id = user
                    tag_connection.userTag_id = tag_obj
                    tag_obj.save()
                    tag_connection.save()
        return redirect("/profile")

def user_password_change(request):
    if request.method == "POST":
        change_form = CustomUserPasswordChangeForm(request.POST, instance=request.user)   
        if change_form.is_valid():
            user = request.user
            if change_form.cleaned_data["old_password"] == user.password:
                user.set_password(change_form.cleaned_data["new_password"])
                user.save()
            else:
                # МБ КАКАЯ-ТО ОБРАБОТКА
                pass
                # redirect("/error")

    if request.method == "GET":
        change_form = CustomUserPasswordChangeForm()
        return render(request, "password.html", {"change_form":change_form})
    return redirect("/profile")

def user_profile(request, pk=None):
    if request.method != "GET":
        return redirect("/error", error_code=400)
    if not pk:
        if request.user.is_authenticated:
            pk = request.user.id
        else:
            redirect("login/")

    user_by_pk = user_app_models.User.objects.get(id=pk)
    tag_connections = user_models.UserTagConnectionTable.objects.filter(user_id=user_by_pk)
    tags = ""
    for connection in tag_connections:
        tag = user_models.UserTag.objects.filter(id=connection.userTag_id.pk).first()
        tags += str(tag.text)

    pages = storage_models.Page.objects.filter(user=user_by_pk)
    print(pages)
    if pk == request.user.id:
        user_form = CustomUserDataChangeForm()
        tag_form = TagForm()
        return render(request, "profile.html", {"user_tags": tags, "user_pages": pages,"user":user_by_pk, "user_form":user_form, "tag_form":tag_form})
    
    return render(request, "profile.html", {"user_tags": tags,"user":user_by_pk,  "user_pages": pages, })
            

def user_delete(request):

    if request.method != "POST":
        return redirect("/profile")
    
    if request.user.is_authenticated:
        delete_form = UserDeleteForm(request.POST)
        if delete_form.is_valid():
            request.user.removed = True
            deleted = user_app_models.UserRemoveDate()
            deleted.remove_date = datetime.now()
            deleted.user_id = request.user
            deleted.save()
            request.user.save()