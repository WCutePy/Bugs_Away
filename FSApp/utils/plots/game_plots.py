from FSApp.models import Click, Game
from datetime import timedelta
from FSApp.utils.plots.click_accuracy_dotplot import create_accuracy_dotplots
from FSApp.utils.plots.click_delta_histogram import create_delta_histogram
from FSApp.utils.plots.clicks_replay import create_replay
from FSApp.utils.plots.click_table import click_table
from pandas import DataFrame


# todo add median and mean data
# todo add data for data table
# todo optimize not sending js for every plot


def get_game_data(user_id, game_id):
    games = Game.objects.filter(
        id=game_id).values(
        "start_time",
        "end_time"
    )

    game_info = [
        (game["start_time"], game["end_time"] - game["start_time"])
        for game in games
    ]

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

    df = DataFrame(
        all_clicks,
        columns=(
            "x", "y", "hit", "dx", "dy", "time", "delta_time_target"
        ),
    )

    return df, game_info


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
            full_html=False, config=config, auto_play=False,
            include_plotlyjs=False,
        ) for fig in plots
    ]


def game_plots(user_id, game_id):
    click_data, game_info = get_game_data(user_id, game_id)

    plots = []

    plots.append(click_table(click_data, game_info))

    plots.extend(create_accuracy_dotplots(click_data))

    plots.append(create_delta_histogram(click_data))

    html = plots_to_html(plots)

    return html


def game_replay(user_id, game_id, click_data=None):
    if click_data is None:
        click_data, _ = get_game_data(user_id, game_id)

    replay = create_replay(click_data)

    html = plots_to_html([replay])

    return html
