from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.


def game_page(request):
    return render(request, "FSApp/pages/game.html")


def stats(request):
    return render(request, "FSApp/pages/stats.html")


def login(request):
    if request.method == "GET":
        return render(request, "FSApp/pages/login.html")


