from FSApp.utils.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import re


def click_table(click_data, game_info):
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
        "accuracy": round(len(hit_data) / len(click_data) * 100, p),
    }

    headers = [
        "Type",
        "Total",
        "Percentage",
        "Mean offset target",
        "Median offset target",
        "Mean time target spawn",
        "Median time target spawn",

    ]

    data = [
        ["hit", "miss", "all"],
        [aggregate_info["hit_amount"], aggregate_info["miss_amount"], aggregate_info["total"]],
        [str(aggregate_info["accuracy"]) + "%",
         str(round(100 - aggregate_info["accuracy"], p)) + "%", "100%"],
        [aggregate_info["hit_mean"], aggregate_info["miss_mean"]],
        [aggregate_info["hit_median"], aggregate_info["miss_median"]],
        [aggregate_info["hit_interval_mean"], "na"],
        [aggregate_info["hit_interval_median"], "na"]

    ]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headers,
            # line_color='darkslategray',
            fill_color='rgba(0, 0, 0, 0)',
        ),
        cells=dict(
            values=data,
            # line_color='darkslategray',
            fill_color='rgba(0, 0, 0, 0)',
        ),
    ),
    ])

    apply_default_layout(fig)

    c_game_info = game_info[0]

    date_string = f"{c_game_info[0].strftime('%Y-%m-%d')} {c_game_info[0].strftime('%H:%M')} UTC"
    game_time_str = re.match(r"^.*\.(..)", str(c_game_info[1])).group(0)[2:]

    fig.update_layout(
        title_text=f"{date_string}<br>"
                   f"duration: {game_time_str}",
        margin_t=65,
        height=220,

    )

    return fig
