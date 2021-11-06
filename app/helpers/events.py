from pygame import USEREVENT


class CustomEvents:
    """Custom PyGame events"""

    ADDED_NEW_STAR = USEREVENT + 1
    CHANGED_STAR_MASS = USEREVENT + 2
