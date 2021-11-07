import pygame
from pygame.math import Vector2

from app.objects import SimulationManager
from app.help.physic import Physic
from app.config import Config


class Grid:
    def __init__(self, color: pygame.Color, distance: int):
        self.surface = pygame.Surface(Config.WINDOW_SIZE, pygame.SRCALPHA)  # lgtm [py/call/wrong-arguments]
        self.color = color  # Grid color
        self.distance = distance  # Distance between dots of grid

    def calculate_grid_dots(self) -> list:
        dots = []
        for x in range(int(Config.WIDTH / self.distance) + 2):
            row = []  # Cleaning up row array
            for y in range(int(Config.HEIGHT / self.distance) + 2):
                position = Vector2(x * self.distance, y * self.distance)  # Position of current dot

                # Calculating offset, based on gravity forces
                offset = Physic.calculate_acceleration(position, SimulationManager.stars) * Config.GRID_CURVATURE
                scaled_offset = Physic.scale_vector(offset, max_length=Config.MAX_GRID_DOT_OFFSET)

                row.append(position + scaled_offset)  # Append offset point to row array
            dots.append(row)  # Append row to dots array

        return dots

    def draw_grid(self, dots: list) -> None:
        # Connecting dots from left to right
        for row in dots:
            for index in range(len(row) - 1):
                pygame.draw.line(self.surface, self.color, row[index], row[index + 1], 1)

        # Connecting dots from top to bottom
        columns = [[row[i] for row in dots] for i in range(len(dots[0]))]
        for column in columns:
            for index in range(len(column) - 1):
                pygame.draw.line(self.surface, self.color, column[index], column[index + 1], 1)
