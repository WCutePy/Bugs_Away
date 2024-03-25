from apscheduler.schedulers.background import BackgroundScheduler
from FSApp.models import CustomUser, UserRecords, Game
from collections import namedtuple
from dataclasses import dataclass
from math import floor

try:
    superuser = CustomUser.objects.create(
        username="admin",
        is_staff=True,  # Set to True to give staff permissions
        is_superuser=True,  # Set to True to give superuser permissions
        profile_picture=0
    )
    superuser.set_password("admin")  # Set the password
    superuser.save()

    user_bozo = CustomUser.objects.get(username='admin')
    default_records = []
    for option in Game.Difficulty.choices:
        default_records.append(UserRecords(user=user_bozo, difficulty=option[0], game=None))
    UserRecords.objects.bulk_create(default_records)
except:
    pass

activeGames = {}
scheduler = BackgroundScheduler(max_instances=1)
scheduler.start()

DEFAULT_TARGET_LENGTH = 5

DEATH_BARRIER_PERCENT = 95

TIMEOUT_TICKS = 200
SECONDS_PER_UPDATE = 0.025

NORMAL_HP = 3

TARGET_SIZE_HALF = 5


@dataclass(frozen=True)
class Difficulty:
    SPEEDS: tuple[float, ...]
    TICKS_PER_SPEED_INCREASE: int
    SPEED_INCREASE: float

    SPAWN_DISTRIBUTION: tuple[float, ...]
    SPAWN_RATE: float
    TICKS_PER_SPAWN_INCREASE: int
    SPAWN_RATE_INCREASE: float


# spawn rate is

easy = Difficulty(
    (1 / 9, 1 / 6, 1 / 4),
    int(20 / SECONDS_PER_UPDATE),
    1 / 25,

    (0.6, 0.3, 0.1),
    0.01,
    int(15 / SECONDS_PER_UPDATE),
    0.0035,
)
medium = Difficulty(
    (1 / 6, 1 / 4, 1 / 2.5),
    int(17.5 / SECONDS_PER_UPDATE),
    1 / 20,

    (0.5, 0.3, 0.2),
    0.025,
    int(15 / SECONDS_PER_UPDATE),
    0.005,
)
hard = Difficulty(
    (1 / 4.5, 1 / 2.5, 1 / 1.75),
    int(15 / SECONDS_PER_UPDATE),
    1 / 17.5,

    (0.3, 0.35, 0.35),
    0.045,
    int(12.5 / SECONDS_PER_UPDATE),
    0.005,
)
DIFFICULTIES = (easy, medium, hard)
