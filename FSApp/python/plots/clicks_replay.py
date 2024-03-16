from FSApp.python.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


interval = 0.01


#todo test if one big dataframe that gets updated every frame,
# so every dot is present all the time, does a not increase size, and b allow transitions

# todo change the length to be dynamic
# todo the bar below needs changing

# todo change popup text
# todo symbol based on hit
# todo the fading in thing looks weird, maybe do away with the size? use the brightness instead


def frame_args(duration=None):
    if duration is None:
        duration = interval * 1000
    return dict(
        frame=dict(
            duration=duration,
            redraw=False,
        ),
        mode="immediate",
        fromcurrent=True,
        transition=dict(
            duration=0, easing="linear"
        ),
    )


def create_replay(click_data: pd.DataFrame):
    pd.options.mode.chained_assignment = None
    file = open("error.txt", "w")

    # file.close()
    frames = []
    sigma = 0.25
    max_size = 20

    sizes = np.linspace(1, 20, int(np.floor(sigma / interval)))
    file.write(str(sizes)+"\n")

    # click_data["time"].max() + sigma
    full_dataframe = pd.DataFrame()

    for t in np.arange(0, 5, interval):
        current_data: pd.DataFrame = click_data[
            (click_data["time"] > t - sigma) & (click_data["time"] < t + sigma)
            ]

        current_data['offset'] = np.abs(current_data['time'] - t)

        # current_data['size'] = (max_size * (1 - (current_data['offset'] / sigma)))
        index = np.round((sizes.size - 1) * (1 - (current_data['offset'] / sigma))).astype(int)
        current_data['size'] = sizes[index]
        current_data['t'] = t

        full_dataframe = pd.concat((full_dataframe, current_data), ignore_index=True)

        if not current_data.empty:
            file.write(f"{t}\n{current_data}\n\n")


        fig = px.scatter(
            current_data, x="x", y="y",
            size="size",
            symbol="hit",
            range_x=[0, 100],
            range_y=[0, 100])

        frames.append(
            go.Frame(data=fig.data, name=str(t))
        )

        if t == 0:
            first_fig = fig

    file.write("\nwriting that frame!\n")
    file.write(str(full_dataframe))

    fig = px.scatter(full_dataframe, x="x", y="y", animation_frame="t", size="size")


    # fig = go.Figure(frames=frames,
    #                 )
    apply_default_layout(fig)

    # fig.add_trace(first_fig.data, )
    # fig.layout = first_fig.layout


    sliders = [
        {
            "pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[f.name], frame_args(0)],
                    "label": str(k),
                    "method": "animate",
                }
                for k, f in enumerate(fig.frames)
            ],
        }
    ]

    axis = dict(
        range=[0, 100],
        tickvals=[0, 50, 100],
        zeroline=False,
        showgrid=False,
    )

    fig.update_layout(
        title_text='Replay',

        xaxis=axis,
        xaxis_title="x",
        yaxis=axis,
        yaxis_title="y",

        scene=dict(
            zaxis=dict(range=[-0.1, 6.8], autorange=False),
            aspectratio=dict(x=1, y=1, z=1),
        ),


        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, frame_args()],
                        "label": "&#9654;",  # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;",  # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
        ],
        sliders=sliders
    )


    return fig
