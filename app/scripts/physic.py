import pygame
from pygame.math import Vector2

from app.scripts.config import Config


class Physic:
    # Scale vector
    @staticmethod
    def scale_vector(vector: Vector2, min_length=None, max_length=None) -> Vector2:
        vector_length = vector.length()

        if min_length is not None:
            if vector_length < min_length:
                vector.scale_to_length(min_length)

        elif max_length is not None:
            if vector_length > max_length:
                vector.scale_to_length(max_length)

        return vector

    # Calculating acceleration
    @staticmethod
    def calculate_acceleration(position_vector: Vector2, objects: pygame.sprite.Group) -> Vector2:
        accelerations = Vector2(0, 0)  # Sum of forces ((0, 0) at the beginning)

        for body in objects:
            vector_distance = Config.K * (body.position_vector - position_vector)

            if vector_distance.length() != 0:
                vector_distance = Physic.scale_vector(vector_distance, min_length=4)  # Scaling vector
                universal_gravity = body.mass / vector_distance.length_squared()  # Calculating magnitude
                unit_vector = (vector_distance / vector_distance.length())  # Calculating unit vector
                acceleration = universal_gravity * unit_vector  # Calculating acceleration

                accelerations += acceleration  # Adding acceleration

        return accelerations
