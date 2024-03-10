from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from re import match
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from FSApp.models import CustomUser, UserPerGame
from django.contrib import messages
from random import randint
from FSApp.python.plots.click_accuracy import click_accuracy_plots

from time import sleep


# Create your views here.

form_fields = (("Username", "text", "[a-zA-Z0-9_.]+", 4, 20),
                          ("Password", "password", ".*", 4, 20))


def game_page(request):
    return render(request, "FSApp/pages/game.html")


def stats(request):
    user_id = request.user.id
    user_games = UserPerGame.objects.filter(user_id=user_id).order_by("-game_id")

    game_info = [(user_game.game.id, user_game.game.start_time, ) for user_game in user_games]
    game_id_1 = game_info[0][0]


    context = {"items": game_info}
    return render(request, "FSApp/pages/stats.html", context)


def personal_game_data(request):
    user_id = request.user.id
    game_id = request.GET.get("game_id")

    if game_id is None:
        return HttpResponseBadRequest("Missing 'game_id' parameter")

    accuracy_plots = click_accuracy_plots(user_id, game_id)

    plots = [
        *accuracy_plots,
    ]

    return JsonResponse({'plots': plots})


def login_view(request):
    context = {"form_tags": form_fields, "name": "login",
               "button_text": "sign in"}

    if request.method == "POST":

        username = request.POST["Username"]
        password = request.POST["Password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

        else:
            try:
                CustomUser.objects.get(username=username)

                messages.error(request, "Incorrect password")
            except CustomUser.DoesNotExist:
                # Username does not exist
                messages.error(request, "Username does not exist")

    if request.user.is_authenticated:
        return redirect(game_page)

    return render(request, "FSApp/pages/login.html", context)


def logout_view(request):

    logout(request)

    return redirect(login_view)


def register_view(request):
    context = {"form_tags": form_fields,
               "name": "register",
               "button_text": "sign up"}

    if request.method == "POST":
        error = []
        for name, _, pattern, minl, maxl in context["form_tags"]:
            field = request.POST.get(name)
            if len(field) < minl or len(field) > maxl:
                messages.error(request, f"{name.title()} is not appropriate length.")
                break
            if not match(pattern, field):
                messages.error(request, f"{name.title()} contains not allowed characters.")
                break

        if not error:
            try:
                user = CustomUser.objects.create_user(
                    username=request.POST.get("Username"),
                    password=request.POST.get("Password"),
                    profile_picture=0
                )

                login(request, user)

                return redirect(game_page)
            except IntegrityError:
                messages.error(request, f"This username is already taken! try: {request.POST.get('Username')+str(randint(1,9999))}")

    return render(request, "FSApp/pages/register.html", context)
