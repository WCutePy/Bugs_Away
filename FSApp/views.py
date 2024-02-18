from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def game(request):
    return render(request, "FSApp/pages/game.html")


def stats(request):
    return render(request, "FSApp/pages/stats.html")


def login(request):
    return HttpResponse("Login not implemented yet")

