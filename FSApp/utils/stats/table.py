from FSApp.utils.stats.default_layout import apply_default_layout
from plotly import graph_objects as go


def default_table(headers, data):
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
    return fig
