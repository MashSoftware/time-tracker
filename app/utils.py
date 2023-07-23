from datetime import time


def seconds_to_string(seconds: int) -> str:
    """Returns the number of seconds formated as a string"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return str(hours) + " h " + str(minutes) + " min"
    elif minutes > 0:
        return str(minutes) + " min"
    else:
        return str(seconds) + "s"


def seconds_to_decimal(seconds: int) -> float:
    """Returns the number of seconds as a float.

    Decimal places are cut off at two, with no rounding.
    """
    decimal = str(round(seconds / 60 / 60, 4)).split(".")
    if len(decimal[1]) > 2:
        decimal[1] = decimal[1][:2]
    return float(".".join(decimal))


def seconds_to_time(seconds: int) -> time:
    """Returns a datetime.time instance for a given number of seconds"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time(hour=hours, minute=minutes, second=seconds)
