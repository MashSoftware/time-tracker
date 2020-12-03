def seconds_to_string(seconds):
    """Returns the number of seconds formated as a string"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return str(hours) + " h " + str(minutes) + " min"
    elif minutes > 0:
        return str(minutes) + " min"
    else:
        return str(seconds) + "s"


def seconds_to_decimal(seconds):
    """Returns the number of seconds as a decimal rounded to two decimal places"""
    return round(seconds / 60 / 60, 2)
