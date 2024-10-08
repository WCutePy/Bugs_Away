"""
URL configuration for FrameShooter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from FSApp import views
from FSApp.utils.game import game_responses
from FSApp.utils.stats import stat_responses

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home),
    path("game", views.game_page),
    path("stats", stat_responses.stats_page),

    path("login", views.login_view),
    path("register", views.register_view),
    path('logout/', views.logout_view, name='logout'),

    path(game_responses.get_game_state.__name__, game_responses.get_game_state),
    path(game_responses.start_game.__name__, game_responses.start_game),
    path(game_responses.receive_click.__name__, game_responses.receive_click),
    path(game_responses.get_end_of_game.__name__, game_responses.get_end_of_game),

    path('personal_game_data/', stat_responses.personal_game_data),
    path('get_replay/', stat_responses.get_replay),

    path("__debug__/", include("debug_toolbar.urls")),
]

