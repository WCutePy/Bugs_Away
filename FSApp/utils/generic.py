from datetime import timedelta


def delta_time_to_string(time: timedelta):
    return (f"{time.seconds // 60:02}m{time.seconds % 60:02}s"
            f"{str(time / timedelta(microseconds=1) % 1000).zfill(0)[:2]}")
