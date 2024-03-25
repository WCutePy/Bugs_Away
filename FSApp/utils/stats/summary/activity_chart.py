import plotly.express as px
import pandas as pd

from FSApp.utils.stats.default_layout import apply_default_layout
from datetime import timedelta


def activity_chart(data: pd.DataFrame):
    # data['hour'] = data['start_time'] / timedelta(hours=1)

    # data['hour_amount'] = data.groupby('hour').sum()

    data['start_time'] = pd.to_datetime(data['start_time'])

    resamples_data = data.resample('6h', on='start_time').size().reset_index(name='games_played')
    resamples_data['end_time'] = resamples_data['start_time'] + pd.Timedelta(hours=6)

    fig = px.line(resamples_data, x='start_time', y='games_played', markers=True)
    fig.update_layout(title='Activity Over Time',
                      xaxis_title='Date',
                      yaxis_title='Number of Games Played')

    hover_data = [(f"Start Time: {start_time.strftime('%b %d %H:%M')} - "
                   f"{'24:00' if end_time.strftime('%H:%M') == '00:00' else end_time.strftime('%H:%M')}"
                   f"<br>Number of Games: {games}")
                  for start_time, end_time, games in zip(resamples_data['start_time'],
                                                         resamples_data['end_time'],
                                                         resamples_data['games_played'])]

    fig.update_traces(hovertemplate=hover_data)

    apply_default_layout(fig)

    return fig
