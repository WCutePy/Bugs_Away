from threading import Thread

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from FSApp.python.game.GameState import GameState
from FSApp.python.game.globals import activeGames
from FSApp.python.game.game_methods import createGame, process_click

from datetime import timedelta


def start_game(request):
    gameId, start_time = createGame()
    request.session["gameId"] = gameId
    return JsonResponse(
        {"gameId": gameId,
         "startTime": start_time
         }
    )


def get_game_state(request):
    gameId = request.session["gameId"]
    cGame: GameState = activeGames[gameId]
    cGame.timeout = 0
    return JsonResponse({
        "targets": cGame.targets,
        "hp": cGame.hp,
        "kills": cGame.kills,
        "terminate": cGame.terminate
    })


@csrf_exempt
def receive_click(request):
    gameId = request.session["gameId"]
    data = request.POST
    cGame: GameState = activeGames[gameId]
    x, y, hitTarget = float(data["x"]), float(data["y"]), data["hitTarget"]
    elapsed_time = data["elapsedTime"]
    targets = cGame.targets[:]

    # thread = Thread(target=process_click,
    #                 args=(x, y, hitTarget, targets, elapsed_time, gameId,
    #                       request.user.id))
    # thread.start()

    process_click(x, y, hitTarget, targets, elapsed_time, gameId,
                  request.user.id)

    return HttpResponse(status=204)
