import pygame
from pygame.math import Vector2

from app.objects import SimulationManager
from app.helpers.physic import Physic
from app.helpers.config import Config


class Grid:
    def __init__(self, color, distance):
        self.surface = pygame.Surface(Config.WINDOW_SIZE, pygame.SRCALPHA)  # lgtm [py/call/wrong-arguments]
        self.color: pygame.Color = color
        self.distance: int = distance

    def calculate_grid_dots(self) -> list:
        dots = []

        for x in range(int(Config.WIDTH / self.distance) + 2):
            row = []
            for y in range(int(Config.HEIGHT / self.distance) + 2):
                position = Vector2(x * self.distance, y * self.distance)
                offset = Physic.calculate_acceleration(position, SimulationManager.stars) * Config.GRID_CURVATURE
                offset = Physic.scale_vector(offset, max_length=Config.MAX_GRID_DOT_OFFSET)

                row.append(position + offset)
            dots.append(row)

        return dots

    def draw_grid(self, dots) -> None:
        # Connecting dots from left to right
        for row in dots:
            for index in range(len(row) - 1):
                pygame.draw.line(self.surface, self.color, row[index], row[index + 1], 1)

        # Connecting dots from top to bottom
        columns = [[row[i] for row in dots] for i in range(len(dots[0]))]
        for column in columns:
            for index in range(len(column) - 1):
                pygame.draw.line(self.surface, self.color, column[index], column[index + 1], 1)

