from datetime import datetime

import pytz
from django.db.models import Count

from FSApp.utils.game.globals import *
from FSApp.utils.game.GameState import GameState
from random import randint, choices, random
from FSApp.models import Game, Click, UserPerGame, CustomUser

from datetime import timedelta


def createGame(difficulty_level: int):
    start_time = datetime.now(pytz.utc)
    game = Game.objects.create(start_time=start_time, difficulty=difficulty_level)
    gameId = game.id
    job = scheduler.add_job(
        updateGameState, "interval", seconds=SECONDS_PER_UPDATE,
        id=str(gameId), args=(gameId, DIFFICULTIES[difficulty_level]))
    activeGames[gameId] = GameState(gameId, job, start_time, difficulty_level)
    cGame: GameState = activeGames[gameId]
    with cGame.lock:
        for i in range(1):
            t = create_target(cGame, DIFFICULTIES[difficulty_level])
            cGame.targets.append(t)

    return gameId, start_time


def endGameJob(gameId):
    end_time = datetime.now(pytz.utc)
    cGame: GameState = activeGames[gameId]
    cGame.job.remove()
    cGame.terminate = True

    game_object = Game.objects.get(id=gameId)
    game_object.end_time = end_time
    game_object.kills = cGame.kills
    game_object.save()

    game_time = end_time - cGame.start_time

    # user_ids = Click.objects.filter(game_id=gameId).values_list('user_id', flat=True).distinct()
    # ids = list(user_ids)

    click_counts = Click.objects.filter(game_id=gameId) \
        .values('user_id') \
        .annotate(click_count=Count('id'))

    user_ids_with_counts = {click['user_id']: click['click_count'] for click in click_counts}
    ids = list(user_ids_with_counts.keys())

    if ids:
        user_id = ids[0]
        UserPerGame.objects.create(user_id=user_id, game_id=gameId, click_count=user_ids_with_counts[user_id])

        file = open("error.txt", "w")
        user_record = UserRecords.objects.filter(user_id=user_id, difficulty=cGame.difficulty).first()
        record_game = user_record.game
        file.write(f"{user_record}\n{user_id}\n{cGame.difficulty}\n{record_game}")
        if record_game is None:
            record_time = timedelta(0)
        else:
            record_time = record_game.end_time - record_game.start_time

        if record_time < game_time:
            user_record.game_id = gameId
            user_record.save()
    cGame.processed = True


def updateGameState(gameId: int, difficulty: Difficulty):
    cGame: GameState = activeGames[gameId]
    cGame.count += 1
    count = cGame.count

    with cGame.lock:
        for target in cGame.targets[:]:
            target[1] += difficulty.SPEEDS[target[4]] + (
                    count // difficulty.TICKS_PER_SPEED_INCREASE) * difficulty.SPEED_INCREASE
            #  refactor formula out of loop ?

            if len(target) > DEFAULT_TARGET_LENGTH:
                cGame.targets.remove(target)
                cGame.kills += 1

            if target[1] > DEATH_BARRIER_PERCENT:
                cGame.targets.remove(target)
                cGame.hp -= 1
                if cGame.hp <= 0:
                    endGameJob(gameId)
                    break
        if (difficulty.SPAWN_RATE + (
                int(count / difficulty.TICKS_PER_SPAWN_INCREASE) * difficulty.SPAWN_RATE_INCREASE)) > random():
            # x y id
            cGame.targets.append(
                create_target(cGame, difficulty)
            )

    cGame.timeout += 1
    if cGame.timeout > TIMEOUT_TICKS:
        endGameJob(gameId)


def create_target(cGame: GameState, difficulty: Difficulty) -> list:
    """_summary_
    0 x
    1 y
    2 unique id
    3 creation time
    4 type id
    """
    type_index = choices(range(0, len(difficulty.SPAWN_DISTRIBUTION)), difficulty.SPAWN_DISTRIBUTION)[0]
    target = [randint(5, 95),
              -5,
              cGame.targetId,
              datetime.now(pytz.utc) - cGame.start_time,
              type_index
              ]
    cGame.targetId += 1

    return target


def process_click(x, y, targets, elapsed_time, gameId, userId):
    closest_target = None
    target_spawned_at = None
    hit = False

    file = open("error.txt", "a")

    delta = 200
    for target in targets:
        tx, ty, tId, t_spawned_at, *_ = target
        n_delta = abs(x - tx) + abs(y - ty)
        if delta > n_delta:
            closest_target = (tx, ty, tId)
            delta = n_delta
        if (tx - TARGET_SIZE_HALF <= x <= tx + TARGET_SIZE_HALF) \
                and (ty - TARGET_SIZE_HALF <= y <= ty + TARGET_SIZE_HALF):
            target_spawned_at = t_spawned_at
            target.append("delete")

    if userId is None:
        return

    if closest_target is not None:
        dx = x - closest_target[0]
        dy = closest_target[1] - y
    else:
        dx = None
        dy = None

    elapsed_time = timedelta(seconds=int(elapsed_time) / 1000)
    elapsed_time_since_target_spawn = None
    if target_spawned_at is not None:
        hit = True
        elapsed_time_since_target_spawn = elapsed_time - target_spawned_at
        file.write(f"{elapsed_time_since_target_spawn} {type(elapsed_time_since_target_spawn)}\n")
    file.write("\n")
    file.close()

    Click.objects.create(frame=1, x=x, y=y, hit=hit,
                         dx=dx, dy=dy,
                         elapsed_time_since_start=elapsed_time,
                         elapsed_time_since_target_spawn=elapsed_time_since_target_spawn,
                         user_id=userId, game_id=gameId)
