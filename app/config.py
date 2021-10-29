"""
Module containing general settings of entire project
"""

# Modules
import pygame
from math import sqrt

# Colors
WHITE = pygame.Color(255, 255, 255)
STAR_COLOR = pygame.Color(255, 255, 17)
PLANET_COLOR = pygame.Color(0, 255, 0)
DARK_BLUE = pygame.Color(0, 6, 15)

BUTTON_GREEN = pygame.Color(121, 190, 112)
BUTTON_RED = pygame.Color(231, 60, 62)

# Window
WIDTH = 1280
HEIGHT = 720
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 120

# Simulation variables
G = 0.0005  # Gravitation constant
# Distance coefficient (square root proportion)
K_value = 1
K = sqrt(K_value)
max_trace_length = 400  # Max length of planet's trace

# Planet preview
pv_radius = 8 // K
pv_line_length_coef = 20 / K
pv_line_thickness = 2
pv_velocity_value_coef = 1 / 80

# Grid settings
grid_distance = 40 / K_value
grid_opacity = 32
grid_color = pygame.Color(155, 155, 155, grid_opacity)
