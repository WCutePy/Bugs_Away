from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.IntegerField()

    def __str__(self):
        return self.username


class Game(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, default=None)

    class Result(models.IntegerChoices):
        UNDEFINED = 0
        IN_PROGRESS = 1
        DEFEAT = 2
        VICTORY = 3

    result = models.IntegerField(choices=Result, default=1)


class Click(models.Model):
    frame = models.IntegerField()
    x = models.DecimalField(max_digits=6, decimal_places=3)
    y = models.DecimalField(max_digits=6, decimal_places=3)
    hit = models.BooleanField()
    dx = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    dy = models.DecimalField(max_digits=6, decimal_places=3, null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['game'], name="game_idx"),
        ]


class UserPerGame(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
