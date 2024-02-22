from FSApp.globals import activeGames
from random import randint


count = 0


def updateGameState(gameId):
    global count
    count += 1
    cGame = activeGames[gameId]
    if count % 10 == 0:
        with cGame[0]:
            for target in cGame[1]:
                target[1] += 1
    if count % 50 == 0:
        with cGame[0]:
            cGame[1].append(
                [randint(0, 91),
                 randint(0, 50),
                 cGame[2]]
            )
            cGame[2] += 1

