from FSApp.python.plots.default_layout import apply_default_layout
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go


def create_replay(x, y, time):
    data = {
        "x": x,
        "y": y,
        "time": time,
    }

    fig = px.scatter(
        data, x="x", y="y", animation_frame="time",
        range_x=[0, 100],
        range_y=[0, 100])

    fig.update_traces(
        mode="markers",
        marker=dict(
            size=10, color="rgba(255, 0, 0, 0.5)",
            symbol="circle"
        )
    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10

    return fig
