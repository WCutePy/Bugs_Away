from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from threading import Lock
from random import randint


# Create your views here.

games = {}

count = 0


def game(request):
    return render(request, "FSApp/pages/game.html")


def stats(request):
    return render(request, "FSApp/pages/stats.html")


def login(request):
    return HttpResponse("Login not implemented yet")


def start_game(request):
    gameId = 1
    games[gameId] = [Lock(), [], 0]
    cGame = games[gameId]
    with cGame[0]:
        for i, a in enumerate(
            ([5, 15, 0], [59, 17, 1], [40, 50, 2], [50, 39, 3])
        ):
            cGame[1].append(a)
            cGame[2] += 1
    return JsonResponse({"gameId": gameId})


def get_game_state(request):
    global count
    count += 1
    cGame = games[1]
    if count % 25 == 0:
        with cGame[0]:
            for target in cGame[1]:
                target[1] += 1
    if count % 125 == 0:
        with cGame[0]:
            cGame[1].append([randint(0, 91), randint(0, 50), cGame[2]])
            cGame[2] += 1
    return JsonResponse({"targets": cGame[1]})


def process_click(request):
    data = request.GET
    cGame = games[1]
    x, y, hitTarget = data["x"], data["y"], data["hitTarget"]

    if hitTarget == "":
        return HttpResponse(status=204)

    hitCompare = int(hitTarget.strip("target"))
    with cGame[0]:
        for target in cGame[1]:
            if target[-1] == hitCompare:
                cGame[1].remove(target)
                break
    return HttpResponse(status=204)
