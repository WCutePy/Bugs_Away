from FSApp.utils.stats.default_layout import apply_default_layout
import plotly.graph_objects as go
import numpy as np


def create_delta_histogram(click_data):

    bin_boundaries = np.arange(0, 4.2, 0.2)
    bin_boundaries[-1] = 100000

    df = click_data[click_data["hit"] == True]

    hist, bins = np.histogram(df["delta_time_target"], bins=bin_boundaries)

    hover_text = [f'{bins[i]:.2f}-{bins[i + 1]:.2f}: {hist[i]}' for i in
                  range(len(hist))]
    hover_text[-1] = f"{bins[-2]:.2f}+: {hist[-1]}"

    num_y_ticks = min(4, max(hist))
    max_y_ticks = int(max(hist)) + 1

    if max_y_ticks <= 2:
        y_ticks = [0, 1]
    else:
        y_ticks = list(
            range(0, max_y_ticks, max_y_ticks // num_y_ticks))

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bins,
        y=hist,
        hoverinfo='text',
        hovertext=hover_text,
        offset=0.02,
    ))

    apply_default_layout(fig)

    fig.update_layout(
        title_text='The interval between target spawn and target hit',
        xaxis=dict(
            title='Time since spawned (seconds)',
            tickvals=bins,
        ),
        yaxis=dict(
            title='Frequency',
            tickvals=y_ticks,
            tickmode='array'
        ),
        showlegend=False,
        # barmode='group', bargap=0, bargroupgap=0.0
    )

    return fig
