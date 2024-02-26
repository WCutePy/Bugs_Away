from apscheduler.schedulers.background import BackgroundScheduler
from FSApp.models import User


try:
    if User.objects.count() == 0:
        User.objects.create(username="John", password="Adams")
except:
    pass


activeGames = {}
scheduler = BackgroundScheduler(max_instances=1)
scheduler.start()


NORMAL_TICKS_PER_MOVE = 1
NORMAL_SPEED = 1/5
NORMAL_TICKS_PER_SPAWN = 50

DEATH_BARRIER_PERCENT = 95

TIMEOUT_TICKS = 200
SECONDS_PER_UPDATE = 0.025

NORMAL_HP = 3

