from django.shortcuts import render
import plotly.graph_objects as go
from FSApp.models import Click


def click_accuracy_plots(user_id, game_id):
    clicks = Click.objects.filter(user_id=user_id, game_id=game_id,
                                  dx__isnull=False).values("dx", "dy", "hit")

    dx_hit = []
    dy_hit = []

    dx_miss = []
    dy_miss = []

    for click in clicks:
        if click["hit"] is True:
            dx_hit.append(click["dx"])
            dy_hit.append(click["dy"])
        else:
            dx_miss.append(click["dx"])
            dy_miss.append(click["dy"])

    plots = []
    plot_vars = (
        (dx_hit, dy_hit),
        (dx_miss, dy_miss)
    )
    for dx, dy in plot_vars:

        fig = go.Figure(data=go.Scatter(x=dx, y=dy, mode='markers'))

        fig.update_layout(
            title='Dot Plot of dx vs dy',
            xaxis=dict(title='dx'),
            yaxis=dict(title='dy'),
        )
        plots.append(fig.to_html(full_html=False))

    return plots

