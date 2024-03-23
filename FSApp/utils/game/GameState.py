from threading import Lock
from FSApp.utils.game.globals import NORMAL_HP
from random import randint


class GameState:
    def __init__(self, gameId, job, start_time, difficulty):
        self.id = gameId
        self.lock = Lock()
        self.targets = []
        self.targetId = 0
        self.job = job
        self.timeout = 0

        self.hp = NORMAL_HP
        self.kills = 0

        self.terminate = False

        self.start_time = start_time
        self.count = 0
        self.difficulty = difficulty

        self.processed = False
