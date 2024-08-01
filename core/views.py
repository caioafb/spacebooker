from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from core.models import *

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "core/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        spacename = request.POST["spacename"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "core/register.html", {
                "message": "As senhas devem coincidir."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "core/register.html", {
                "message": "Nome de usuário indisponível."
            })
        
        # Create new Space and sets the user as admin
        space = Space(name=spacename, admin=user)
        space.save()
        user.space = space
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "core/register.html")
    
@login_required
def index(request):
    space = request.user.space
    return render(request, "core/index.html", {
        "space": space
    })

@login_required
def schedule(request):
    if request.method == "POST":
        pass

    return render(request, "core/schedule.html", {
        "users": request.user.space.space_users.all(),
        "space": request.user.space
    })

@login_required
def settings(request):
    message = None
    error = None
    users = request.user.space.space_users.all().exclude(id=request.user.id)

    if request.method == "POST":
        if request.POST["option"] == "insert_user":
            username = request.POST["username"]
            email = request.user.email

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "core/settings.html", {
                    "error": "As senhas devem coincidir.",
                    "users": users
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.space = request.user.space
                user.save()
            except IntegrityError:
                return render(request, "core/settings.html", {
                    "error": "Nome de usuário indisponível.",
                    "users": users
                })
            message = "Usuário cadastrado com sucesso."

        elif request.POST["option"] == "delete_user":
            user = User.objects.get(id = request.POST["deleted_user"])
            user.delete()
            message = "Usuário removido com sucesso."

    return render(request, "core/settings.html", {
        "users": users,
        "message": message,
        "error": error
    })