from FSApp.utils.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# todo investigate, slider not always showing up when time below 1 sec
# todo figure the fuck out why timing doesn't work, and how to scale it
# todo scale time to minute and seconds


def create_replay(click_data: pd.DataFrame):
    pd.options.mode.chained_assignment = None

    interval = 0.05  # seconds
    sigma = 0.25
    max_size = 15

    debugging = False
    if debugging:
        max_time = 1
    else:
        max_time = click_data["time"].max() + sigma

    sizes = np.linspace(1, max_size, int(np.floor(sigma / interval)))
    if len(sizes) < 2:
        sizes = [max_size]
    full_dataframe = pd.DataFrame()

    for t in np.arange(0, max_time, interval):
        current_data: pd.DataFrame = click_data[
            (click_data["time"] > t - sigma) & (click_data["time"] < t + sigma)
            ]

        # current_data['offset'] = np.abs(current_data['time'] - t)
        # current_data['size'] = (max_size *
        #                         (1 - (current_data['offset'] / sigma)))
        # index = np.round((sizes.size - 1) *
        #             (1 - (current_data['offset'] / sigma))).astype(int)
        # current_data['size'] = sizes[index]
        current_data['size'] = max_size

        current_data['original_index'] = click_data.index[current_data.index]

        if current_data.empty:


            current_data = click_data.iloc[[0]]
            current_data['size'] = 0
            current_data['original_index'] = -1
        current_data['t'] = t

        full_dataframe = pd.concat((full_dataframe, current_data),
                                   ignore_index=True)

    full_dataframe["y"] = 100 - full_dataframe["y"]
    full_dataframe["hitstr"] = full_dataframe["hit"].astype(str)

    mapping = {True: 0, False: 1}
    full_dataframe["color"] = full_dataframe["hit"].map(mapping)

    colors = ("rgb(59, 130, 246)", "red")
    hit_color, miss_color = colors

    fig = px.scatter(
        full_dataframe,
        x="x",
        y="y",
        animation_frame="t",
        animation_group="original_index",
        size="size",

        color="color",
        color_continuous_scale=[[0, hit_color], [1, miss_color]],
        range_color=[0, 1],


        hover_data=dict(
            x=True,
            y=True,
            t=False,
            size=False,
            hit=True,
        ),
    )

    apply_default_layout(fig)

    def frame_args(duration=None):
        if duration is None:
            duration = interval * 100
        return dict(
            frame=dict(
                duration=duration,
                redraw=False,
            ),
            mode="immediate",
            fromcurrent=True,
            transition=dict(
                duration=duration,
                # easing="linear"
            ),
        )

    sliders = [
        dict(
            pad=dict(b=10, t=60),
            len=0.9,
            x=0.1,
            y=0,
            steps=[
                dict(
                    args=[[f.name], frame_args()],
                    label=str(round(k * interval, 2)),
                    method="animate"
                )
                for k, f in enumerate(fig.frames)
                # if (k % int((max_time / interval) / 50)) == 0 or k == 0
            ],
            transition=dict(
                duration=0,
                # easing="linear"
            ),
            tickcolor="white",


        )
    ]

    text = ("hit", "miss")
    for i, color in enumerate(colors):
        y_offset = i * 0.05
        x_base = 1.1
        y_base = 0.95
        fig.add_annotation(
            xref="paper", yref="paper",
            x=x_base,
            y=y_base - y_offset,
            text=text[i],
            showarrow=False,
            xanchor='left',
        )
        size = 0.02
        x_circle = x_base - 0.03
        y_circle = y_base - 0.009
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=x_circle, x1=x_circle + size,
            y0=y_circle - y_offset, y1=y_circle - size - y_offset,
            line=dict(
                color=color,
            ),
            fillcolor=color,
        )


    axis = dict(
        range=[0, 100],
        tickvals=[0, 50, 100],
        zeroline=False,
        showgrid=False,
        position=0,
        automargin=True,
        minallowed=0,
        maxallowed=100,
    )

    fig.update_layout(
        title_text='Replay',
        showlegend=False,
        # legend=dict(
        # ),
        margin_r=150,
        hovermode=False,

        xaxis=dict(
            **axis,
            title="x",
        ),
        yaxis=dict(
            **axis,
            title="y",
            scaleanchor="x",
        ),
        width=700,
        height=700,

        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[None, frame_args()],
                        label="&#9654;",  # play symbol
                        method="animate"
                    ),
                    dict(
                        args=[[None], frame_args(0)],
                        label="&#9724;",  # pause symbol
                        method="animate"
                    )
                ],
                direction="left",
                pad=dict(r=10, t=70),
                type="buttons",
                x=0.1,
                y=0,
                borderwidth=0,
            )
        ],
        sliders=sliders
    )

    return fig
