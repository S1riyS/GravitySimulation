"""
Module containing objects classes of simulations objects
"""

# Modules
import copy
from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2

from app.config import *


# Simulation manager class
class SimulationManager:
    # Surfaces with elements of simulation
    glow_surface = pygame.Surface(Config.WINDOW_SIZE).convert_alpha()
    trace_surface = pygame.Surface(Config.WINDOW_SIZE).convert_alpha()

    # Sprite groups
    celestial_bodies = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    stars = pygame.sprite.Group()


# Main simulation class
class SimulationObject(pygame.sprite.Sprite):
    """
    Main Class of simulation.
    Inherited from PyGame Sprite Class.
    """

    __ID = 1  # Each object of simulation has ID

    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.id = SimulationObject.__ID

        self.x = x  # X coordinate
        self.y = y  # Y coordinate
        self.color = color  # Color

        SimulationObject.__ID += 1  # Increasing ID by 1


# Celestial body class
class CelestialBody(SimulationObject, ABC):
    """
    Class that contains general settings of 'celestial bodies'.
    Inherited from SimulationObject and ABC Classes.
    """

    def __init__(self, x, y, mass, color):
        super().__init__(x, y, color)

        self.mass = mass
        self.glow_color = copy.copy(self.color)  # Without alpha

        SimulationManager.celestial_bodies.add(self)

    @abstractmethod
    def get_radius(self, mass: int) -> float:
        """Abstract method, that returns radius, based on object's mass"""
        pass

    # Set object's surface, rect and image
    def set_rect(self):
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius)).convert_alpha()
        self.image.fill((0, 0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.position_vector = Vector2(self.rect.centerx, self.rect.centery)

    def draw_object_body(self):
        pygame.draw.circle(
            self.image,  # Surface
            self.color,  # Color
            (self.image.get_width() // 2, self.image.get_height() // 2),  # Relative position
            self.radius  # Object radius
        )

    def draw_object_glow(self, glow_radius: int, glow_color: pygame.Color, glow_layers: int):
        """
        Method in which the glow is drawn
        :param glow_radius: Max radius of glowing
        :param glow_color: Color of glowing
        :param glow_layers: Number of layers of glowing
        :return: None
        """

        # Glow surface
        surface_side = 2 * (self.radius + glow_radius)
        self.current_glow_surface = pygame.Surface((surface_side, surface_side)).convert_alpha()
        self.current_glow_surface.fill((0, 0, 0, 0))
        center_of_surface = (surface_side // 2, surface_side // 2)

        current_glow_color = glow_color  # Setting current color

        for i in range(glow_layers):
            # Calculating color of glow
            current_glow_alpha = min(Config.BASE_GLOW_ALPHA * (i + 1), 255)  # Calculated alpha (from 0 to 255)
            current_glow_color.a = current_glow_alpha  # Setting alpha to current color

            pygame.draw.circle(
                self.current_glow_surface,  # Surface
                current_glow_color,  # Color
                center_of_surface,  # Relative position
                self.radius + glow_radius * ((glow_layers - i) / glow_layers)  # Glow radius
            )

        # Drawing glow on a screen
        position = (self.rect.centerx - self.radius - glow_radius, self.rect.centery - self.radius - glow_radius)
        SimulationManager.glow_surface.blit(self.current_glow_surface, position)  # Drawing glow on screen


# Planet class
class Planet(CelestialBody):
    """
    Class that describing fields and methods of 'Planets'.
    Inherited from CelestialBody Class.
    """

    def __init__(self, x, y, velocity, mass, color):
        """
        :param x: Initial X coordinate
        :param y: Initial Y coordinate
        :param velocity: 2D vector with initial velocity
        :param mass: Mass of the planet
        :param color: Color of the planet
        """

        super().__init__(x, y, mass, color)
        self.radius = self.get_radius(self.mass)  # Radius of planet
        self.set_rect()
        self.draw_object_body()

        self.glow_radius = self.radius  # Size of glow
        self.trace_color = copy.copy(self.color)
        self.trace_color.a = Config.BASE_TRACE_ALPHA

        self.traces = [(self.x, self.y)]  # Array of dots
        self.MAX_TRACE_LENGTH = 400  # Max size of array
        self.velocity = velocity  # Set initial velocity

        SimulationManager.planets.add(self)

    def get_radius(self, mass: int) -> float:
        radius = 8 // Config.K * (mass / Config.PLANET_DEFAULT_MASS) ** (1 / 3)
        return radius

    @staticmethod
    def scale_vector(vector: Vector2, min_length: int, max_length=None) -> Vector2:
        vector_length = vector.length()

        if vector_length < min_length:
            new_vector = vector * (min_length / vector_length)
            return new_vector

        elif max_length is not None:
            if vector_length > max_length:
                new_vector = vector * (max_length / vector_length)
                return new_vector

        return vector

    # Updating position
    def update_position(self, dt):
        self.accelerations = Vector2(0, 0)  # Sum of forces ((0, 0) at the beginning)
        self.position_vector = Vector2(self.x, self.y)  # Position vector

        for body in SimulationManager.celestial_bodies:
            if body.id != self.id:
                vector_distance = Config.K * (body.position_vector - self.position_vector)
                vector_distance = self.scale_vector(vector_distance, min_length=3)

                if vector_distance.length() == 0:
                    print(
                        f'№{self.id} and №{body.id} - killed by collision with each other, '
                        f'position: {self.position_vector}'
                    )
                    self.kill()
                    body.kill()

                else:
                    universal_gravity = body.mass / vector_distance.length_squared()
                    unit_vector = (vector_distance / vector_distance.length())
                    acceleration = universal_gravity * unit_vector  # Gravitational force between this body and another

                    self.accelerations += acceleration  # Adding this force

        self.velocity += Config.G * self.accelerations * dt  # Adding forces to velocity

        # Applying velocity changes
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        self.rect.centerx = self.x
        self.rect.centery = self.y

    # Collision with stars
    def collision_with_stars(self):
        for star in SimulationManager.stars:
            vector_distance = star.position_vector - self.position_vector
            if vector_distance.length() < (star.radius + self.radius):
                star.devour(self)  # Start 'devouring this planet'
                print(f'№{self.id} - killed by collision with star, position: {self.position_vector}')
                self.kill()

    # Is planet out of system
    def is_out_of_system(self):
        max_coefficient = 8
        if abs(self.rect.x) > Config.WIDTH * max_coefficient or abs(self.rect.y) > Config.HEIGHT * max_coefficient:
            print(f'№{self.id} - killed by out of system, position: {self.position_vector}')
            self.kill()

    # Drawing planet trace
    def draw_trace(self):
        # Deleting unnecessary positions
        if len(self.traces) > Config.MAX_TRACE_LENGTH:
            difference = len(self.traces) - Config.MAX_TRACE_LENGTH
            self.traces = self.traces[difference:]

        previous_pos = self.traces[0]

        for index, pos in enumerate(self.traces):
            line_thickness = min(index // 100 + 1, 3)  # Calculated value or 3
            pygame.draw.line(SimulationManager.trace_surface, self.trace_color, previous_pos, pos,
                             line_thickness)  # Drawing line
            previous_pos = pos  # Setting previous position

    def update(self, *args, **kwargs) -> None:
        delta_time = kwargs.get('dt') * Config.STABLE_FPS
        # Adding new position to trace array
        if delta_time > 0:
            position = (self.rect.centerx, self.rect.centery)
            self.traces.append(position)

        # Updating
        self.update_position(dt=delta_time)
        self.collision_with_stars()
        self.is_out_of_system()
        self.draw_trace()
        self.draw_object_glow(glow_radius=self.glow_radius, glow_color=self.glow_color, glow_layers=3)


# Star class
class Star(CelestialBody):
    """
    Class that describing 'Stars'.
    Inherited from CelestialBody Class.
    """

    def __init__(self, x, y, mass, color):
        super().__init__(x, y, mass, color)
        self.radius = self.get_radius(self.mass)
        self.glow_radius = self.radius * 0.7  # Size of glow
        self.set_rect()
        self.draw_object_body()  # Drawing body of Star

        SimulationManager.stars.add(self)

    def get_radius(self, mass: int) -> float:
        radius = (30 // Config.K) * (mass / Config.STAR_DEFAULT_MASS) ** (1 / 2)
        return radius

    def devour(self, planet: Planet) -> None:
        self.mass += Config.DEVOUR_COEFFICIENT * planet.mass

        self.radius = self.get_radius(self.mass)
        self.glow_radius = self.radius * 0.7  # Size of glow

        self.set_rect()
        self.draw_object_body()  # Drawing body of Star

    def update(self, *args, **kwargs) -> None:
        self.draw_object_glow(glow_radius=self.glow_radius, glow_color=self.glow_color, glow_layers=5)
