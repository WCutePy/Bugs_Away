from threading import Lock
from FSApp.game.schedules import updateGameState


class GameState:
    def __init__(self, gameId, scheduler):
        self.id = gameId
        self.lock = Lock()
        self.targets = []
        self.targetId = 0
        self.job = scheduler.add_job(
            updateGameState, "interval", seconds=0.025,
            id=str(gameId), args=(gameId,))
        self.timeout = 0
