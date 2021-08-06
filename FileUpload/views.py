import json
import os
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from FileUpload.models import UserDataModel


def add_pagination(request, all_data):
    page = request.GET.get('page', 1)
    paginator = Paginator(all_data, 10)
    try:
        all_data = paginator.page(page)
    except PageNotAnInteger:
        all_data = paginator.page(1)
    except EmptyPage:
        all_data = paginator.page(paginator.num_pages)
    return all_data


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                messages.success(request, "congo 😊 user registered successfully..")
                return redirect("login")
            except IntegrityError:
                messages.error(request, "username already taken..")
                return render(request, "register.html", {"form": UserCreationForm()})
        else:
            messages.error(request, "The two password fields didn't match.")
            return render(request, "register.html", {"form": UserCreationForm()})


def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            messages.error(request, "username and password didn't match")
            return render(request, "login.html", {"form": AuthenticationForm()})
        else:
            auth_login(request, user)
            return redirect("userhome")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")


@login_required
def userhome(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('user_json_file')
        fs = FileSystemStorage()

        if not os.path.isfile("media/{}".format(uploaded_file.name)):
            fs.save(uploaded_file.name, uploaded_file)
            financepeer_json_data = "media/{}".format(uploaded_file.name)
            f = open(financepeer_json_data, 'r')
            financepeer_json_data = json.load(f)

            objs = [
                UserDataModel.objects.create(userid="{}".format(i["userId"]), uid="{}".format(i["id"]),
                                             title="{}".format(i["title"]),
                                             body="{}".format(i["body"]))
                for i in financepeer_json_data]
            UserDataModel.objects.bulk_update(objs, ["userid", "uid", "title", "body"])

    final_data = add_pagination(request, UserDataModel.objects.all().order_by('id'))

    context = {
        "all_users_data": final_data
    }
    return render(request, "userhome.html", context=context)
