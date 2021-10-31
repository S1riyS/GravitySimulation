"""
Module containing objects classes of simulations objects
"""

# Modules
import copy

import pygame
from pygame.math import Vector2

from app.config import *


class SimulationManager:
    def __init__(self):
        # Surface with some objects of simulation
        self.glow_surface = pygame.Surface(WINDOW_SIZE).convert_alpha()
        self.trace_surface = pygame.Surface(WINDOW_SIZE).convert_alpha()

        # Sprite groups
        self.celestial_bodies = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()


simulation_manager = SimulationManager()


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
class CelestialBody(SimulationObject):
    """
    Class that contains general settings of 'celestial bodies'.
    Inherited from SimulationObject Class.
    """

    def __init__(self, x, y, mass, color):
        super().__init__(x, y, color)

        self.mass = mass
        self.glow_color = copy.copy(self.color)  # Without alpha

        simulation_manager.celestial_bodies.add(self)

    # Set object's surface, rect and image
    def set_rect(self, radius: int):
        self.radius = radius
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
            current_glow_alpha = min(BASE_GLOW_ALPHA * (i + 1), 255)  # Calculated alpha (from 0 to 255)
            current_glow_color.a = current_glow_alpha  # Setting alpha to current color

            pygame.draw.circle(
                self.current_glow_surface,  # Surface
                current_glow_color,  # Color
                center_of_surface,  # Relative position
                self.radius + glow_radius * ((glow_layers - i) / glow_layers)  # Glow radius
            )

        # Drawing glow on a screen
        position = (self.rect.centerx - self.radius - glow_radius, self.rect.centery - self.radius - glow_radius)
        simulation_manager.glow_surface.blit(self.current_glow_surface, position)  # Drawing glow on screen


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
        planet_radius = 8 // K * (self.mass / 150) ** (1 / 3)  # Radius of planet
        self.set_rect(radius=planet_radius)
        self.draw_object_body()

        self.glow_radius = planet_radius  # Size of glow
        self.trace_color = copy.copy(self.color)
        self.trace_color.a = BASE_TRACE_ALPHA

        self.traces = [(self.x, self.y)]  # Array of dots
        self.max_trace_length = 400  # Max size of array
        self.velocity = velocity  # Set initial velocity

        simulation_manager.planets.add(self)

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

        for body in simulation_manager.celestial_bodies:
            if body.id != self.id:
                vector_distance = K * (body.position_vector - self.position_vector)
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

        self.velocity += G * self.accelerations * dt  # Adding forces to velocity

        # Applying velocity changes
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        self.rect.centerx = self.x
        self.rect.centery = self.y

    # Collision with stars
    def collision_with_stars(self):
        for star in simulation_manager.stars:
            vector_distance = star.position_vector - self.position_vector
            if vector_distance.length() < (star.radius + self.radius):
                print(f'№{self.id} - killed by collision with star, position: {self.position_vector}')
                self.kill()

    # Is planet out of system
    def is_out_of_system(self):
        max_coefficient = 8
        if abs(self.rect.x) > WIDTH * max_coefficient or abs(self.rect.y) > HEIGHT * max_coefficient:
            print(f'№{self.id} - killed by out of system, position: {self.position_vector}')
            self.kill()

    # Drawing planet trace
    def draw_trace(self):
        # Deleting unnecessary positions
        if len(self.traces) > max_trace_length:
            difference = len(self.traces) - max_trace_length
            self.traces = self.traces[difference:]

        previous_pos = self.traces[0]

        for index, pos in enumerate(self.traces):
            line_thickness = min(index // 100 + 1, 3)  # Calculated value or 3
            pygame.draw.line(simulation_manager.trace_surface, self.trace_color, previous_pos, pos,
                             line_thickness)  # Drawing line
            previous_pos = pos  # Setting previous position

    def update(self, *args, **kwargs) -> None:
        delta_time = kwargs.get('dt') * FPS_CONST
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
        star_radius = (30 // K) * (self.mass / 20000) ** (1 / 2)
        self.set_rect(radius=star_radius)

        self.glow_radius = star_radius * 0.7  # Size of glow

        self.draw_object_body()  # Drawing body of Star

        simulation_manager.stars.add(self)

    def update(self, *args, **kwargs) -> None:
        self.draw_object_glow(glow_radius=self.glow_radius, glow_color=self.glow_color, glow_layers=5)
