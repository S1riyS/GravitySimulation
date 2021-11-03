"""
Module containing general settings of entire project
"""

# Modules
from pygame import Color

class Config:
    # Colors
    WHITE = Color(255, 255, 255)
    STAR_COLOR = Color(255, 255, 17)
    PLANET_COLOR = Color(0, 255, 0)
    DARK_BLUE = Color(0, 6, 15)
    TRANSPARENT = Color(0, 0, 0, 0)

    BUTTON_GREEN = Color(47, 191, 113)
    BUTTON_RED = Color(239, 45, 86)

    # Window
    WIDTH = 1280
    HEIGHT = 720
    WINDOW_SIZE = (WIDTH, HEIGHT)
    FPS = 120
    STABLE_FPS = 100

    # Simulation variables
    G = 0.075  # Gravitation constant
    # Distance coefficient (square root proportion)
    K = 1
    MAX_TRACE_LENGTH = 400  # Max length of planet's trace

    # Simulation objects' settings
    BASE_GLOW_ALPHA = 20
    BASE_TRACE_ALPHA = 255

    # Planet settings
    PLANET_DEFAULT_MASS = 150
    PLANET_MIN_MASS = 50
    PLANET_MAX_MASS = 450

    # Star settings
    STAR_DEFAULT_MASS = 20000
    STAR_MIN_MASS = 10000
    STAR_MAX_MASS = 30000
    DEVOUR_COEFFICIENT = 10

    # Planet preview
    PV_RADIUS = 8 // K
    PV_LENGTH_COEF = 20 / K
    PV_LINE_THICKNESS = 2
    PV_VELOCITY_COEF = 1 / 80

    # Grid settings
    GRID_DISTANCE = 40 / K
    GRID_OPACITY = 32
    GRID_COLOR = Color(155, 155, 155, GRID_OPACITY)
