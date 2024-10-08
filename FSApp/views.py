import random
import string

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from re import match
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from FSApp.models import CustomUser, UserPerGame, Game, UserRecords
from django.contrib import messages
from random import randint
from FSApp.utils.stats.individual_game.game_plots import game_plots, game_replay

import io, base64
from PIL import Image

# Create your views here.

form_fields = (("Username", "text", "[a-zA-Z0-9_.]+", 4, 20),
               ("Password", "password", ".*", 4, 20))


def game_page(request):
    return render(request, "FSApp/pages/game.html")


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
        error = False
        for name, _, pattern, minl, maxl in context["form_tags"]:
            field = request.POST.get(name)
            if len(field) < minl or len(field) > maxl:
                messages.error(request, f"{name.title()} is not appropriate length.")
                error = True
                break
            if not match(pattern, field):
                messages.error(request, f"{name.title()} contains not allowed characters.")
                error = True
                break

        image_data = request.POST.get('image_data')
        try:
            img = Image.open(
                io.BytesIO(base64.decodebytes(bytes(image_data, "utf-8"))))

        except:
            error = True
            messages.error(request, "Please provide a png or jpg image.")

        if not error:
            try:
                filename = ''.join(random.choices(string.ascii_letters + string.digits, k=32)) + ".png"

                img.save(rf"FSApp\static\FSApp\img\pp\{filename}")

                user = CustomUser.objects.create_user(
                    username=request.POST.get("Username"),
                    password=request.POST.get("Password"),
                    profile_picture=0,
                    profile_picture_string=filename,
                )

                default_records = []
                for option in Game.Difficulty.choices:
                    default_records.append(UserRecords(user=user, difficulty=option[0], game=None))
                UserRecords.objects.bulk_create(default_records)

                login(request, user)

                return redirect(game_page)
            except IntegrityError:
                messages.error(request,
                               f"This username is already taken! try: {request.POST.get('Username') + str(randint(1, 9999))}")

    return render(request, "FSApp/pages/register.html", context)


def test(request):
    return render(request, "FSApp/pages/test.html")


def home(request):
    return render(request, "FSApp/pages/home.html")
