from django.shortcuts import render
import plotly.graph_objects as go
from FSApp.models import Click
from plotly.offline import plot
from datetime import timedelta
from FSApp.utils.plots.click_accuracy_dotplot import create_accuracy_dotplots
from FSApp.utils.plots.click_delta_histogram import create_delta_histogram
from FSApp.utils.plots.clicks_replay import create_replay
from FSApp.utils.plots.click_table import click_table
from pandas import DataFrame


# todo add median and mean data
# todo add data for data table
# todo optimize not sending js for every plot


def get_game_data(user_id, game_id) -> DataFrame:
    clicks = Click.objects.filter(
        user_id=user_id, game_id=game_id,
        dx__isnull=False).values(
        "x", "y",
        "dx", "dy",
        "hit",
        "elapsed_time_since_start",
        "elapsed_time_since_target_spawn")

    all_clicks = []

    for click in clicks:
        delta_time_target = None
        if click["hit"] is True:
            delta_time_target = click["elapsed_time_since_target_spawn"] \
                                 / timedelta(seconds=1)

        all_clicks.append((
            click["x"],
            click["y"],
            click["hit"],
            click["dx"],
            click["dy"],
            click["elapsed_time_since_start"].total_seconds(),
            delta_time_target,
        ))

    return DataFrame(all_clicks, columns=("x", "y", "hit", "dx", "dy",
                                          "time", "delta_time_target"))


def plots_to_html(plots):
    config = dict(
        displayModeBar=False,
        editable=False,
        scrollZoom=False,
        showAxisDragHandles=False,
        showAxisRangeEntryBoxes=False,
        autosizable=False,
    )
    return [
        fig.to_html(
            full_html=False, config=config, auto_play=False
        ) for fig in plots
    ]


def game_plots(user_id, game_id):
    click_data = get_game_data(user_id, game_id)

    hit_data = click_data[click_data["hit"] == True]
    miss_data = click_data[click_data["hit"] == False]

    p = 1 # precision
    aggregate_info = {
        "total": len(click_data),
        "hit_amount": len(hit_data),
        "hit_mean": (round(hit_data["dx"].mean(), p),
                     round(hit_data["dy"].mean(), p)),
        "hit_median": (round(hit_data["dx"].median(), p),
                       round(hit_data["dy"].median(), p)),
        "hit_interval_mean": round(hit_data["delta_time_target"].mean(), p),
        "hit_interval_median": round(hit_data["delta_time_target"].median(), p),
        "miss_amount": len(miss_data),
        "miss_mean": (round(miss_data["dx"].mean(), p),
                      round(miss_data["dy"].mean(), p)),
        "miss_median": (round(miss_data["dx"].median()),
                        round(miss_data["dy"].median())),
        "accuracy": f"{round(len(hit_data) / len(click_data) * 100, p)} %",
    }

    plots = []

    plots.append(click_table(aggregate_info))

    plots.extend(create_accuracy_dotplots(click_data))

    plots.append(create_delta_histogram(click_data))

    html = plots_to_html(plots)


    return html, aggregate_info


def game_replay(user_id, game_id, click_data=None):
    if click_data is None:
        click_data = get_game_data(user_id, game_id)

    replay = create_replay(click_data)

    html = plots_to_html([replay])

    return html
