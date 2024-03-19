from threading import Thread

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from FSApp.utils.game.GameState import GameState
from FSApp.utils.game.globals import activeGames
from FSApp.utils.game.game_methods import createGame, process_click
from FSApp.models import CustomUser

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
    gameId = int(request.GET.get("gameId"))
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
    data = request.POST
    gameId = int(data["gameId"])
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


def get_end_of_game(request):
    gameId = request.session["gameId"]

    user = CustomUser.objects.get(id=request.user.id)
    record_id = user.record_id
    record = user.record.end_time - user.record.start_time

    formatted_record = (f"{record.seconds // 60:02}m{record.seconds % 60:02}s"
                        f"{str(record / timedelta(microseconds=1)  % 1000).zfill(0)[:2]}")


    return JsonResponse({"record": formatted_record, "current": gameId == record_id})
