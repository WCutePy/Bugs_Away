from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    profile_picture = models.IntegerField(default=0)


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
    x = models.DecimalField(max_digits=6, decimal_places=3)
    y = models.DecimalField(max_digits=6, decimal_places=3)
    frame = models.IntegerField()
    hit = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
