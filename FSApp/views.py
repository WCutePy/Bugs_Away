from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from threading import Lock
from random import randint
from FSApp.globals import activeGames, scheduler
from FSApp.schedules import updateGameState


# Create your views here.

tempGameId = 0

count = 0


def game(request):
    return render(request, "FSApp/pages/game.html")


def stats(request):
    return render(request, "FSApp/pages/stats.html")


def login(request):
    return HttpResponse("Login not implemented yet")


def start_game(request):
    global tempGameId
    tempGameId += 1
    gameId = tempGameId
    activeGames[gameId] = [
        Lock(),
        [],
        0,
        scheduler.add_job(updateGameState, "interval", seconds=0.025,
                          id=str(gameId), args=(gameId,))
    ]
    cGame = activeGames[gameId]
    with cGame[0]:
        for i, a in enumerate(
            ([5, 15, 0], [59, 17, 1], [40, 50, 2], [50, 39, 3])
        ):
            cGame[1].append(a)
            cGame[2] += 1
    return JsonResponse({"gameId": gameId})


def get_game_state(request):
    global count
    cGame = activeGames[tempGameId]
    return JsonResponse({"targets": cGame[1]})


def process_click(request):
    data = request.GET
    cGame = activeGames[tempGameId]
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
