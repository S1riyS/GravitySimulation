"""
Module containing general settings of entire project
"""

# Modules
import pygame
from math import sqrt

# Colors
BLACK = pygame.Color(12, 12, 12)
WHITE = pygame.Color(255, 255, 255)

RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(252, 255, 17)

LIGHT_GREEN = pygame.Color(144, 238, 144)
FOREST_GREEN = pygame.Color(0, 255, 0)

BLUE = pygame.Color(0, 0, 255)
DARK_BLUE = pygame.Color(0, 6, 15)

# Window
WIDTH = 1280
HEIGHT = 720
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 120

# Game settings
screen = pygame.display.set_mode(WINDOW_SIZE)
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
