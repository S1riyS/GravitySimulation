"""
Module containing objects classes of simulations objects
"""

# Modules
from copy import copy
from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2

from app.helpers.physic import Physic
from app.helpers.config import Config


# Simulation manager class
class SimulationManager:
    # Surfaces with elements of simulation
    glow_surface = pygame.Surface(Config.WINDOW_SIZE, pygame.SRCALPHA)  # lgtm [py/call/wrong-arguments]
    trace_surface = pygame.Surface(Config.WINDOW_SIZE, pygame.SRCALPHA)  # lgtm [py/call/wrong-arguments]

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
        self.glow_color = copy(self.color)  # Without alpha

        SimulationManager.celestial_bodies.add(self)

    # Set object's surface, rect and image
    def set_object_rect(self, radius):
        self.image = pygame.Surface((2 * radius, 2 * radius)).convert_alpha()  # lgtm [py/call/wrong-arguments]
        self.image.fill(Config.TRANSPARENT)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.position_vector = Vector2(self.rect.centerx, self.rect.centery)

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
        self.current_glow_surface = pygame.Surface((surface_side, surface_side)).convert_alpha() # lgtm [py/call/wrong-arguments]
        self.current_glow_surface.fill(Config.TRANSPARENT)
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
                self.radius + glow_radius * (1 - i / glow_layers)  # Glow radius
            )

        # Drawing glow on a screen
        position = (self.rect.centerx - self.radius - glow_radius, self.rect.centery - self.radius - glow_radius)
        SimulationManager.glow_surface.blit(self.current_glow_surface, position)  # Drawing glow on screen

    @staticmethod
    @abstractmethod
    def get_radius(mass: int) -> float:
        """Method, that returns radius, based on object's mass"""
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Method, that updates object every tick"""
        pass


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
        self.set_object_rect(self.radius)

        self.glow_radius = self.radius  # Size of glow
        self.trace_color = copy(self.color)
        self.trace_color.a = Config.BASE_TRACE_ALPHA

        self.traces = [(self.x, self.y)]  # Array of dots
        self.MAX_TRACE_LENGTH = 400  # Max size of array
        self.velocity = velocity  # Set initial velocity

        SimulationManager.planets.add(self)

    @staticmethod
    def get_radius(mass: int) -> float:
        radius = 8 // Config.K * (mass / Config.PLANET_DEFAULT_MASS) ** (1 / 3)
        return radius

    # Updating position
    def update_position(self, dt):
        self.acceleration = Vector2(0, 0)  # Sum of forces ((0, 0) at the beginning)
        self.position_vector = Vector2(self.x, self.y)  # Position vector

        self.acceleration = Physic.calculate_acceleration(self.position_vector, SimulationManager.celestial_bodies)

        self.velocity += Config.G * self.acceleration * dt  # Adding forces to velocity

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
                print(f'№{self.id} - killed by collision with star, position: {self.position_vector}')
                star.devour(self)  # Star 'devouring this planet'
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
        self.set_object_rect(self.radius)
        self.glow_radius = self.radius * 0.7  # Size of glow

        SimulationManager.stars.add(self)
        pygame.event.post(pygame.event.Event(Config.ADDED_NEW_STAR))

    @staticmethod
    def get_radius(mass: int) -> float:
        radius = (30 // Config.K) * (mass / Config.STAR_DEFAULT_MASS) ** (1 / 2)
        return radius

    def devour(self, planet: Planet) -> None:
        self.mass += Config.DEVOUR_COEFFICIENT * planet.mass

        self.radius = self.get_radius(self.mass)
        self.set_object_rect(self.radius)
        self.glow_radius = self.radius * 0.7  # Size of glow

    def update(self, *args, **kwargs) -> None:
        self.draw_object_glow(glow_radius=self.glow_radius, glow_color=self.glow_color, glow_layers=5)
