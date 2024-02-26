from datetime import datetime
from threading import Thread

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from FSApp.game.GameState import GameState
from FSApp.game.globals import activeGames, scheduler
from FSApp.game.game_methods import createGame, process_click



def start_game(request):
    gameId = createGame()
    request.session["gameId"] = gameId
    return JsonResponse({"gameId": gameId})


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
    targets = cGame.targets[:]

    # scheduler.add_job(process_click, "date", run_date=datetime.now(),
    #                   args=(x, y, hitTarget, targets, gameId))

    thread = Thread(target=process_click,
                    args=(x, y, hitTarget, targets, gameId))
    thread.start()

    return HttpResponse(status=204)


