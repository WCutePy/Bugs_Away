from FSApp.utils.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import pandas as pd


#todo make the two line up, cuz it doesn't look good when switching quickly rn

def create_accuracy_dotplots(click_data: pd.DataFrame):
    plots = []

    hit = click_data[click_data["hit"] == True]
    miss = click_data[click_data["hit"] == False]

    dotplot_vars = (
        ("Distance from the middle of the target hit",
         hit["dx"], hit["dy"], 7.5,
         (-5, 0, 5),),
        ("Distance from the closest target",
         miss["dx"], miss["dy"], 37.5,
         (-25, 0, 25),)
    )
    for title, dx, dy, size_range, ticks in dotplot_vars:
        fig = go.Figure(
            data=go.Scatter(
                x=dx, y=dy,
                mode='markers',
                marker=dict(
                    size=7,
                )
            )
        )
        apply_default_layout(fig)

        middle_scale = size_range / 10

        line_ranges = [
            (
                (middle_scale, 0),
                (100, 0)
            ),
        ]
        [line_ranges.append(((y, x), (y2, x2))) for ((x, y), (x2, y2))
         in line_ranges[:]]
        for (ax, ay), (bx, by) in line_ranges:
            fig.add_shape(type='line',
                          x0=-bx, y0=-by, x1=bx, y1=by,
                          line=dict(
                              color='white', width=1, dash="dot",
                          ),
                          layer="below",
                          )

            fig.add_shape(type='line',
                          x0=-ax, y0=-ay, x1=ax, y1=ay,
                          line=dict(color="red", width=2),
                          layer="below",
                          )
        # tick_text = [(3 - len(str(num))) * "a" + str(num) for num in ticks]

        axis = dict(
            range=(-size_range, size_range),
            minallowed=-size_range,
            maxallowed=size_range,
            zeroline=False,
            tickvals=ticks,
            # ticktext=tick_text,
            showgrid=False,
            # showspikes=True,
        )
        fig.update_layout(
            title=dict(
                text=title,
            ),

            xaxis=axis,
            yaxis=axis,
            xaxis_title="dx (%)",
            yaxis_title="dy (%)",
            yaxis_scaleanchor="x",
            width = 500,
            height= 500,
        )

        plots.append(fig)
    return plots
