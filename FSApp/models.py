from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models import UniqueConstraint


# Create your models here.


class Game(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, default=None)

    class Difficulty(models.IntegerChoices):
        EASY = 0
        MEDIUM = 1
        HARD = 2
    difficulty = models.IntegerField(choices=Difficulty.choices, default=Difficulty.EASY)


class CustomUser(AbstractUser):
    profile_picture = models.IntegerField()
    profile_picture_string = models.CharField(max_length=40, null=False,
                                              default="kale.jpg")

    def __str__(self):
        return self.username


class Click(models.Model):
    frame = models.IntegerField()
    x = models.DecimalField(max_digits=6, decimal_places=3)
    y = models.DecimalField(max_digits=6, decimal_places=3)
    hit = models.BooleanField()
    dx = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    dy = models.DecimalField(max_digits=6, decimal_places=3, null=True)

    elapsed_time_since_start = models.DurationField(null=True)
    elapsed_time_since_target_spawn = models.DurationField(null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['game'], name="game_idx"),
        ]   


class UserPerGame(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class UserRecords(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    difficulty = models.IntegerField(choices=Game.Difficulty)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'difficulty'], name="user difficulty"),
        ]
