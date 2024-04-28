from django.shortcuts import render, redirect
from storage_app.forms import *
from storage_app import models
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

# Create your views here.

def upload_files(request):

    if not request.user.is_authenticated:
        return redirect("/error", error_code=403)
    
    if request.method == "POST":

        file_upload_form = FileUploadForm(request.POST, request.FILES)
        if file_upload_form.is_valid():

            page = models.Page()
            page.user = request.user
            page.title = file_upload_form.cleaned_data['title']
            page.image = file_upload_form.cleaned_data['image']
            page.public_on = file_upload_form.cleaned_data['public_on']
            page.comment_on = file_upload_form.cleaned_data['comments_on']
            page.save()
            page_type="other"
            all_files_end = None
            for f in request.FILES.getlist('files'):

                file = models.File()
                file.path = f
                file.comment_on = file_upload_form.cleaned_data['comments_on']
                file.link_on = file_upload_form.cleaned_data['link_on']
                file.public_on = file_upload_form.cleaned_data['public_on']
                file.save()
                print((str(file.path)), "- file format")
                if (str(file.path)).lower().endswith(".mp3"):
                    if all_files_end != None:
                        if all_files_end != ".mp3":
                            all_files_end = "MIXED"
                    else:
                        all_files_end = ".mp3"
                elif (str(file.path)).lower().endswith(".mp4"):
                    if all_files_end != None:
                        if all_files_end != ".mp4":
                            all_files_end = "MIXED"
                    else:
                        all_files_end = ".mp4"
                else:
                    all_files_end = "MIXED"

                if file_upload_form.cleaned_data['link_on'] == True:

                    link = models.Link()
                    link.file = file
                    link.save()

                filepage = models.FilePage()
                filepage.file = file
                filepage.page = page
                filepage.save()

            if all_files_end != "MIXED":
                if all_files_end == ".mp3":
                    page_type = "music"
                else:
                    page_type = "video"
            
            page.category = page_type
            page.save()

        return redirect("/upload")
    
    elif request.method == "GET":

        form = FileUploadForm()
        return render(request, "upload.html", {"upload_form":form})

def page(request, page_id=None):
    if page_id:
        if request.method == "GET":
            do_owner = False
            if request.user.is_authenticated:
                page = models.Page.objects.get(id=page_id)
                if not page:
                    return redirect("/error")
                
                if request.user == page.user:
                    do_owner = True

            files = []
            page = models.Page.objects.get(id=page_id)
            filepage_query = models.FilePage.objects.filter(page=page)
            for filepage in filepage_query:
                file = models.File.objects.get(id=filepage.file.id)
                if not file.public_on:
                    if do_owner:
                        files.append(file)
                files.append(file)

            return render(request, "page.html", {'files':files, 'do_owner':do_owner})

    return redirect("/error")

def file_page(request, file_id):
    if file_id:
        if request.method == "GET":
            do_owner = False
            file = models.File.objects.get(id=file_id)
            if not file:
                return redirect("/error")
            if request.user.is_authenticated:
                filepage = models.FilePage.objects.get(file=file)
                page = models.Page.objects.get(id=filepage.page.id)
                if request.user == page.user:
                    do_owner = True

            if not file.public_on:
                if not do_owner:
                    return redirect("/error", error_code=401)
            return render(request, "file.html", {'file':file, 'do_owner':do_owner})
    else:
        return redirect("/error")

def link_page(request, link_id):
    if link_id:
        if request.method == "GET":
            do_owner = False
            link = models.Link.objects.get(id=link_id)
            file = models.File.objects.get(id=link.file.id)
            if not link:
                return redirect("/error")
            if request.user.is_authenticated:
                filepage = models.FilePage.objects.get(file=file)
                page = models.Page.objects.get(id=filepage.page.id)
                if request.user == page.user:
                    do_owner = True

            file = models.File.objects.get(id=link.file.id)

            return render(request, "file.html", {'file':file, 'do_owner':do_owner})
        
    return redirect("/error")

def delete_file(request, file_id):
    if request.method == "POST":
        if file_id:
            if request.user.is_authenticated:
                file = models.File.objects.get(id=file_id)
                filepage= models.FilePage.objects.get(file=file)
                page = models.Page.objects.get(id=filepage.page.id)
                if request.user == page.user:
                    file.delete()
                    filepages = models.FilePage.objects.filter(page=page)
                    if filepages.count() == 0:
                        page.delete()
                        return redirect("/")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            return redirect("/error", error_code=403)
        return redirect("/error")
    return redirect("/error", error_code=400)

@cache_page(1)
def main_view(request):
    if request.method == "GET":

        response = None
        result_page = None

        if request.user.is_authenticated:
            result_page = "main_logged.html"
        else:
            result_page = "main_unlogged.html"

        response = render(request, result_page, {"user": request.user})
        response.set_cookie('message', "Thank you for choosing us!")

        return response
    else:
        return redirect("error/", error_code=400, message="Bad request")

# render/redirect to "error/" without params if code 404
def error_page(request, error_code=404, message=None):
    if request.method == "GET":
        if message == None:
            match error_code:
                case 400: message="Bad request"
                case 401: message="Unauthorized"
                case 403: message="Forbiden"
                case 404: message="Page not found"

            message = "Page not found"
        return render(request, "error.html", {"error_code":error_code, "message":message})
    return redirect("error/")

def pagination_pro(request):

    category = request.POST.get('text')
    search = request.POST.get('search')

    my_model = None
    my_model = models.Page.objects.all()

    if category:
        my_model = my_model.filter(category=category)
    if search:
        my_model = my_model.filter(name=search)

    my_model = my_model.order_by('-id')

    #number of items on each page
    number_of_item = 9 # желательно кратное 3, тк 3 столбца
    
    #Paginator
    paginatorr = Paginator(my_model, number_of_item)
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range

    context = {
    'paginatorr':paginatorr,
    'first_page':first_page,
    'page_range':page_range
    }

    if request.method == 'POST':

        page_n = request.POST.get('page_n', None) #getting page number
        results = list(paginatorr.page(page_n).object_list.values('id', 'title', 'image'))
        return JsonResponse({"results":results})

    return render(request, 'index.html', context)