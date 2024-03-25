from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from FSApp.models import UserPerGame
from FSApp.utils.stats.individual_game.game_plots import game_plots, game_replay
from FSApp.utils.stats.summary.activity_chart import activity_chart
from FSApp.utils.stats.summary.get_data import get_data
from FSApp.utils.stats.default_layout import plots_to_html


def stats_page(request):
    user_id = request.user.id
    sidebar_data, games_data, records_data = get_data(user_id)

    context = {
        "items": sidebar_data,
        "total_games": len(games_data),
        "clicks": games_data["clicks"].sum(),
        "kills": games_data["kills"].sum(),
        "records": records_data
    }

    if user_id is None:
        messages.error(request, "Please login")
    elif len(sidebar_data) == 0:
        messages.error(request, "Please play some games ")
    else:
        activity = activity_chart(games_data)
        plot_html = plots_to_html(
            [activity],
            config=dict()
        )
        context["activity_chart"] = plot_html[0]

    return render(request, "FSApp/pages/stats.html", context)


def personal_game_data(request):
    user_id = request.user.id
    game_id = request.GET.get("game_id")

    if game_id is None:
        return HttpResponseBadRequest("Missing 'game_id' parameter")

    html_plots = game_plots(user_id, game_id)

    return JsonResponse({'plots': html_plots})


def get_replay(request):
    user_id = request.user.id
    game_id = request.GET.get("game_id")

    if game_id is None:
        return HttpResponseBadRequest("Missing 'game_id' parameter")

    replay = game_replay(user_id, game_id)

    return JsonResponse({"replay": replay})
