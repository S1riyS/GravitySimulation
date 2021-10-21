"""
Module containing general settings of entire project
"""
# Modules
import pygame
from math import sqrt

# Colors
BLACK = (12, 12, 12)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)
FOREST_GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 15)
YELLOW = (252, 255, 17)

# Window
WIDTH = 1280
HEIGHT = 720
FPS = 120

# Game settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()

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
