from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def game(request):
    return render(request, "FSApp/pages/game.html")


def stats(request):
    return HttpResponse("stats not implemented yet")


def login(request):
    return HttpResponse("Login not implemented yet")

