"""
Module containing general settings of entire project
"""

# Modules
from pygame import Color
from math import sqrt

# Colors
WHITE = Color(255, 255, 255)
STAR_COLOR = Color(255, 255, 17)
PLANET_COLOR = Color(0, 255, 0)
DARK_BLUE = Color(0, 6, 15)

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
K_value = 1
K = sqrt(K_value)
max_trace_length = 400  # Max length of planet's trace

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
pv_radius = 8 // K
pv_line_length_coef = 20 / K
pv_line_thickness = 2
pv_velocity_value_coef = 1 / 80

# Grid settings
grid_distance = 40 / K_value
grid_opacity = 32
grid_color = Color(155, 155, 155, grid_opacity)
