from django.contrib import admin

# Register your models here.
from .models import CustomUser, Game, Click, UserPerGame

admin.site.register(CustomUser)
admin.site.register(Game)
admin.site.register(Click)
admin.site.register(UserPerGame)
