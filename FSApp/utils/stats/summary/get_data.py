from django.db.models import Prefetch

from FSApp.models import Game
from FSApp.models import CustomUser, Game, UserRecords, UserPerGame
import pandas as pd
from FSApp.utils.generic import delta_time_to_string


def get_data(user_id):
    games_queryset = UserPerGame.objects.filter(user_id=user_id).select_related("game")

    overview_data = []
    game_data = []
    for user_game in games_queryset:
        overview_data.append((
            user_game.game.id,
            user_game.game.start_time,
            delta_time_to_string(user_game.game.end_time - user_game.game.start_time),
        ))
        game_data.append((
            user_game.game.start_time,
            user_game.game.end_time - user_game.game.start_time,
            user_game.game.kills,
            user_game.click_count,
            user_game.game.difficulty,
        ))
    df = pd.DataFrame(
        game_data,
        columns=("start_time", "duration", "kills", "clicks", "difficulty"),
    )

    # records_queryset = UserRecords.objects.filter(user_id=user_id).select_related("game")
    # currenty no extra database query is done, as the data is already loaded
    # there is no guarantee that this is better than another query.
    file = open("error", "w")
    record_data = []
    for difficulty, _ in Game.Difficulty.choices:
        durations = df[df["difficulty"] == difficulty]["duration"]
        file.write(f"{durations}\n")
        if durations.empty:
            record_data.append(None)
        else:
            record_index = durations.idxmax()
            record = (
                overview_data[record_index][0],
                df.loc[record_index, "start_time"],
                delta_time_to_string(df.loc[record_index, "duration"]),
            )
            record_data.append(record)

    file.write(f"{record_data}")
    return overview_data[::-1], df, record_data

