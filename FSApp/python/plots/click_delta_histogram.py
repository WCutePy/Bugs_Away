from FSApp.python.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import numpy as np


def create_delta_histogram(delta_time_target):

    bin_boundaries = [0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                      1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0]
    bin_boundaries = np.arange(0, 4, 0.2)

    hist, bins = np.histogram(delta_time_target, bins=bin_boundaries)

    hover_text = [f'{bins[i]:.2f}-{bins[i + 1]:.2f}: {hist[i]}' for i in
                  range(len(hist))]

    num_y_ticks = min(4, max(hist))
    max_y_ticks = int(max(hist)) + 1

    if max_y_ticks <= 2:
        y_ticks = [0, 1]
    else:
        y_ticks = list(
            range(0, max_y_ticks, max_y_ticks // num_y_ticks))

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bins[:-1],
        y=hist,
        hoverinfo='text',
        hovertext=hover_text,

    ))

    apply_default_layout(fig)

    fig.update_layout(
        title_text='The interval between target spawn and target hit',
        xaxis=dict(
            title='Delta time (seconds)',
            dtick=0.25,
        ),
        yaxis=dict(
            title='Frequency',
            tickvals=y_ticks,
            tickmode='array'
        ),
        showlegend=False,
        barmode='group', bargap=0.3, bargroupgap=0.0
    )

    return fig
