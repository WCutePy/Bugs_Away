from django.http import HttpResponse, JsonResponse
from FSApp.game.globals import activeGames, scheduler
from FSApp.game.GameState import GameState

tempGameId = 0

count = 0


def start_game(request):
    # game = Game(start_time=datetime.now(pytz.utc))

    global tempGameId
    tempGameId += 1
    gameId = tempGameId
    activeGames[gameId] = GameState(gameId, scheduler)
    cGame: GameState = activeGames[gameId]
    with cGame.lock:
        for i, a in enumerate(
            ([5, 15, 0], [59, 17, 1], [40, 50, 2], [50, 39, 3])
        ):
            cGame.targets.append(a)
            cGame.targetId += 1
    return JsonResponse({"gameId": gameId})


def get_game_state(request):
    global count
    cGame: GameState = activeGames[tempGameId]
    cGame.timeout = 0
    return JsonResponse({"targets": cGame.targets})


def process_click(request):
    data = request.GET
    cGame: GameState = activeGames[tempGameId]
    x, y, hitTarget = data["x"], data["y"], data["hitTarget"]

    if hitTarget != "":
        hitCompare = int(hitTarget.strip("target"))
        with cGame.lock:
            for target in cGame.targets:
                if target[-1] == hitCompare:
                    cGame.targets.remove(target)
                    break

    return HttpResponse(status=204)
