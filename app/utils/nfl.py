from datetime import datetime


def get_current_nfl_season():
    """
    NFL season starts in September.
    Jan-Aug belong to the previous season.
    """

    today = datetime.now()

    if today.month >= 9:
        return today.year

    return today.year - 1