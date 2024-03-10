from datetime import datetime

import pytz

from FSApp.python.game.globals import \
    activeGames, NORMAL_SPEED, NORMAL_TICKS_PER_MOVE, \
    NORMAL_TICKS_PER_SPAWN, \
    DEATH_BARRIER_PERCENT, TIMEOUT_TICKS, scheduler, SECONDS_PER_UPDATE
from FSApp.python.game.GameState import GameState
from random import randint
from FSApp.models import Game, Click, UserPerGame

count = 0


def createGame():
    start_time = datetime.now(pytz.utc)
    game = Game.objects.create(start_time=start_time)
    gameId = game.id
    job = scheduler.add_job(
            updateGameState, "interval", seconds=SECONDS_PER_UPDATE,
            id=str(gameId), args=(gameId,))
    activeGames[gameId] = GameState(gameId, job)
    cGame: GameState = activeGames[gameId]
    with cGame.lock:
        for i, a in enumerate(
                ([5, 15, 0], [59, 17, 1], [40, 50, 2], [50, 39, 3])
        ):
            cGame.targets.append(a)
            cGame.targetId += 1

    return gameId, start_time


def endGameJob(gameId, result=None):
    cGame: GameState = activeGames[gameId]
    cGame.job.remove()
    cGame.terminate = True
    # activeGames.pop(gameId)
    end_time = datetime.now(pytz.utc)
    game_object = Game.objects.get(id=gameId)
    game_object.end_time = end_time

    if result is None:
        if cGame.hp <= 0:
            result = Game.Result.DEFEAT
        else:
            result = Game.Result.UNDEFINED

    game_object.result = result
    game_object.save()

    user_ids = Click.objects.filter(game_id=gameId).values_list('user_id', flat=True).distinct()
    ids = list(user_ids)
    if ids:
        UserPerGame.objects.create(user_id=ids[0], game_id=gameId)


def updateGameState(gameId):
    global count
    count += 1
    cGame: GameState = activeGames[gameId]
    with cGame.lock:
        if count % NORMAL_TICKS_PER_MOVE == 0:
            for target in cGame.targets:
                target[1] += NORMAL_SPEED
        if count % NORMAL_TICKS_PER_SPAWN == 0:
            # x y id
            cGame.targets.append(
                [randint(5, 95),
                 randint(5, 45),
                 cGame.targetId]
            )
            cGame.targetId += 1
        for target in cGame.targets[:]:
            if len(target) > 3:
                cGame.targets.remove(target)
                cGame.kills += 1
            if target[1] > DEATH_BARRIER_PERCENT:
                cGame.targets.remove(target)
                cGame.hp -= 1
                if cGame.hp == 0:
                    endGameJob(gameId)
    cGame.timeout += 1
    if cGame.timeout > TIMEOUT_TICKS:
        endGameJob(gameId)


def process_click(x, y, hitTarget, targets, gameId, userId):
    closest_target = None

    if hitTarget != "":
        hitCompare = int(hitTarget.strip("target"))
        for target in targets:
            if target[-1] == hitCompare:
                closest_target = tuple(target)
                target.append("delete")
                break

    if userId is None:
        return

    if hitTarget == "":
        delta = 200
        for (tx, ty, tId) in targets:
            n_delta = abs(x - tx) + abs(y - ty)
            if delta > n_delta:
                closest_target = (tx, ty, tId)
                delta = n_delta

    if closest_target is not None:
        dx = x - closest_target[0]
        dy = y - closest_target[1]
    else:
        dx = None
        dy = None

    Click.objects.create(frame=1, x=x, y=y, hit=bool(hitTarget),
                         dx=dx, dy=dy,
                         user_id=userId, game_id=gameId)
