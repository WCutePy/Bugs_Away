from FSApp.python.plots.default_layout import apply_default_layout
import plotly.graph_objects as go


def create_accuracy_dotplots(dx_hit, dy_hit, dx_miss, dy_miss):
    plots = []

    dotplot_vars = (
        ("Distance from the middle of the target on hit", dx_hit, dy_hit, 7.5,
         (-5, 0, 5),),
        ("Distance from the target on a miss", dx_miss, dy_miss, 35,
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

        axis = dict(
            title='dx',
            range=(-size_range, size_range),
            zeroline=False,
            tickvals=ticks,
            showgrid=False,
        )
        fig.update_layout(
            title=dict(
                text=title,
            ),
            xaxis=axis,
            yaxis=axis,
        )

        plots.append(fig)
    return plots
