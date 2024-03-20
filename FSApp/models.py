from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Game(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, default=None)

    class Result(models.IntegerChoices):
        UNDEFINED = 0
        IN_PROGRESS = 1
        DEFEAT = 2
        VICTORY = 3

    result = models.IntegerField(choices=Result, default=1)


class CustomUser(AbstractUser):
    profile_picture = models.IntegerField()
    record = models.ForeignKey(Game, on_delete=models.SET_NULL,
                               null=True, blank=True, default=None)
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
