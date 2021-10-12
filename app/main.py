# Modules
import pygame
from pygame.math import Vector2
import pygame_gui

from config import *
from objects import *

pygame.init()

manager = pygame_gui.UIManager((WIDTH, HEIGHT))  # GUI manager

# GUI
velocity_x_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 10, 200, 20),
                                               text='X velocity: None', manager=manager)
velocity_y_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 35, 200, 20),
                                               text='Y velocity: None', manager=manager)
G_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 60, 200, 20),
                                      text='G = ' + str(G), manager=manager)
K_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 85, 200, 20),
                                      text='Distance coef = ' + str(K_value), manager=manager)


# Game loop
run = True
while run:
    screen.fill(DARK_BLUE)
    clock.tick(FPS)
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_position[0], mouse_position[1]

            if event.button == 3:
                Star(
                    x=mouse_x,
                    y=mouse_y,
                    mass=10000,
                    color=YELLOW)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                try:
                    Planet(
                        x=mouse_x,
                        y=mouse_y,
                        velocity_x=velocity_vector.x,
                        velocity_y=velocity_vector.y,
                        mass=150,
                        color=FOREST_GREEN
                    )

                    velocity_x_label.set_text('X velocity: None')
                    velocity_y_label.set_text('Y velocity: None')

                except Exception as error:
                    print('Velocity vector is not defined')

    pressed = pygame.mouse.get_pressed()  # Pressed buttons
    if pressed[0]:
        # Mouse position (x, y)
        mouse_position = pygame.mouse.get_pos()
        current_mouse_x, current_mouse_y = mouse_position[0], mouse_position[1]

        # Calculating velocity vector
        current_pos_vector = Vector2(current_mouse_x, current_mouse_y)
        pressed_pos_vector = Vector2(mouse_x, mouse_y)
        velocity_vector = -(current_pos_vector - pressed_pos_vector) * pv_velocity_value_coef

        # Setting labels
        velocity_x_label.set_text('X velocity: ' + str(round(velocity_vector.x, 4)))
        velocity_y_label.set_text('Y velocity: ' + str(round(velocity_vector.y, 4)))

        # Drawing preview
        pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), pv_radius)
        pygame.draw.line(screen, WHITE,
                         (mouse_x, mouse_y),
                         (mouse_x + velocity_vector.x * pv_line_length_coef,
                          mouse_y + velocity_vector.y * pv_line_length_coef), pv_line_thickness)

        manager.process_events(event)

    # Updating screen and groups of sprites
    celestial_bodies.update()
    celestial_bodies.draw(screen)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
