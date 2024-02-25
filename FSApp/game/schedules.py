from FSApp.game.globals import activeGames
from random import randint


count = 0


def updateGameState(gameId):
    global count
    count += 1
    cGame = activeGames[gameId]
    with cGame.lock:
        if count % 5 == 0:
            for target in cGame.targets:
                target[1] += 1
        if count % 50 == 0:
            cGame.targets.append(
                [randint(0, 90),
                 randint(0, 50),
                 cGame.targetId]
            )
            cGame.targetId += 1
        for target in cGame.targets[:]:
            if target[1] > 90:
                cGame.targets.remove(target)
    cGame.timeout += 1
    if cGame.timeout > 200:
        cGame.job.remove()
        activeGames.pop(gameId)
