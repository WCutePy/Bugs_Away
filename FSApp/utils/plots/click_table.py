from FSApp.utils.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


def click_table(aggregate_info: dict):
    data = [
        ["Total Clicks", aggregate_info["total"]],
        ["Hits", aggregate_info["hit_amount"]],
        ["Mean of Hits (dx, dy)", aggregate_info["hit_mean"]],
        ["Median of Hits (dx, dy)", aggregate_info["hit_median"]],
        ["Mean Time for Hits", aggregate_info["hit_interval_mean"]],
        ["Median Time for Hits", aggregate_info["hit_interval_median"]],
        ["Misses", aggregate_info["miss_amount"]],
        ["Mean of Misses (dx, dy)", aggregate_info["miss_mean"]],
        ["Median of Misses (dx, dy)", aggregate_info["miss_median"]],
        ["Accuracy", aggregate_info["accuracy"]],
    ]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Metric", "Value"],
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

    fig.update_layout(
        title_text="Aggregate Information Table",

    )

    return fig
