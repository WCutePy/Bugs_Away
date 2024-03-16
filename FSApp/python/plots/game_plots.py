from django.shortcuts import render
import plotly.graph_objects as go
from FSApp.models import Click
from plotly.offline import plot
from datetime import timedelta
from FSApp.python.plots.click_accuracy_dotplot import create_accuracy_dotplots
from FSApp.python.plots.click_delta_histogram import create_delta_histogram
from FSApp.python.plots.clicks_replay import create_replay
from pandas import DataFrame


def game_plots(user_id, game_id):
    clicks = Click.objects.filter(
        user_id=user_id, game_id=game_id,
        dx__isnull=False).values(
        "x", "y",
        "dx", "dy", "hit", "elapsed_time_since_start",
        "elapsed_time_since_target_spawn")

    dx_hit = []
    dy_hit = []

    dx_miss = []
    dy_miss = []

    time = []

    delta_time_target_hit = []

    all_clicks = []

    for click in clicks:
        if click["hit"] is True:
            dx_hit.append(click["dx"])
            dy_hit.append(click["dy"])

            delta_time_target_hit.append(
                click["elapsed_time_since_target_spawn"] / timedelta(seconds=1)
            )

        else:
            dx_miss.append(click["dx"])
            dy_miss.append(click["dy"])

        all_clicks.append((
            click["x"],
            click["y"],
            click["hit"],
            click["dx"],
            click["dy"],
            click["elapsed_time_since_start"].total_seconds()
        ))

    click_data = DataFrame(all_clicks, columns=("x", "y", "hit", "dx", "dy",
                                                "time"))

    plots = []

    plots.extend(create_accuracy_dotplots(dx_hit, dy_hit, dx_miss, dy_miss))

    plots.append(create_delta_histogram(delta_time_target_hit))

    plots.append(create_replay(click_data))

    config = dict(
        displayModeBar=False,
        editable=False,
        scrollZoom=False,
        showAxisDragHandles=False,
        showAxisRangeEntryBoxes=False,
        autosizable=False,
    )

    html = (
        fig.to_html(
            full_html=False, config=config, auto_play=False
        ) for fig in plots
    )
    return html
