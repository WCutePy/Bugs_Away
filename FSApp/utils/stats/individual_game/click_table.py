from FSApp.utils.stats.default_layout import apply_default_layout
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import re
from FSApp.templatetags.FSApp_extras import difficulty_names

from FSApp.utils.stats.table import default_table


def click_table(click_data, game_info, game_id):
    hit_data = click_data[click_data["hit"] == True]
    miss_data = click_data[click_data["hit"] == False]

    p = 1  # precision
    aggregate_info = {
        "total": len(click_data),
        "hit_amount": len(hit_data),
        "miss_amount": len(miss_data),
        "accuracy": round(len(hit_data) / len(click_data) * 100, p),
    }

    headers = [
        "Type",
        "Total",
        "Percentage",
    ]

    data = [
        ["hit", "miss", "all"],
        [aggregate_info["hit_amount"], aggregate_info["miss_amount"],
         aggregate_info["total"]],
        [str(aggregate_info["accuracy"]) + "%",
         str(round(100 - aggregate_info["accuracy"], p)) + "%", "100%"],
    ]

    fig = default_table(headers, data)

    c_game_info = game_info[0]

    date_string = f"{c_game_info[0].strftime('%Y-%m-%d')} {c_game_info[0].strftime('%H:%M')} UTC"
    game_time_str = re.match(r"^.*\.(..)", str(c_game_info[1])).group(0)[2:]

    fig.update_layout(
        title_text=f"Game: {game_id}<br>{date_string}<br>Difficulty: {difficulty_names()[c_game_info[2]]}<br>"
                   f"duration: {game_time_str}",
        margin_t=140,
        height=260,
    )

    return fig
