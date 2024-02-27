from threading import Lock
from FSApp.game.globals import NORMAL_HP


class GameState:
    def __init__(self, gameId, job):
        self.id = gameId
        self.lock = Lock()
        self.targets = []
        self.targetId = 0
        self.job = job
        self.timeout = 0

        self.hp = NORMAL_HP
        self.kills = 0

        self.terminate = False