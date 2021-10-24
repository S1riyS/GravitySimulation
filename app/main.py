"""
Main project file, that containing game loop
"""

# Modules
import pygame
from pygame.math import Vector2
import pygame_gui

from app.config import *
from app.gui import GUIManager  # Importing entire GUI

pygame.init()


class Game:
    def __init__(self):
        # PyGame screen variables
        self.screen = pygame.display.set_mode(WINDOW_SIZE)  # Initialize screen
        pygame.display.set_caption("Gravity Simulation")  # Caption
        self.clock = pygame.time.Clock()  # Clock

        # ----- GUI ----- #
        self.gui_manager = GUIManager()

        # Info block
        self.info_gui_rect = self.gui_manager.get_gui_rect(self.gui_manager.info_block, 10)
        self.info_gui_elements = self.gui_manager.info_block['elements_dict']
        self.info_gui_elements['FPS_counter'].bg_colour = pygame.Color('#1b2933')
        self.info_gui_elements['FPS_counter'].font = pygame.font.Font(None, 26)

    @staticmethod
    def mouse_collision_with_gui(mouse_position: tuple, gui_rects: list) -> bool:
        """
        Return True if mouse on any of GUI rects and False if it isn't
        :param gui_rects:
        :param mouse_position:
        :return: bool
        """

        return any([rect.collidepoint(mouse_position) for rect in gui_rects])

    def run(self):
        # Import everything necessary from objects
        from app.objects import simulation_surface, celestial_bodies, Planet, Star

        # Game loop
        run = True
        while run:
            # Filling surfaces
            simulation_surface.fill((0, 0, 0, 0))
            self.screen.fill(DARK_BLUE)

            self.clock.tick(FPS)
            self.time_delta = self.clock.tick(FPS) / 1000.0

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse position
                    pressed_mouse_position = pygame.mouse.get_pos()
                    mouse_x, mouse_y = pressed_mouse_position
                    # Checking if mouse on GUI
                    is_mouse_on_gui = self.mouse_collision_with_gui(
                        mouse_position=pressed_mouse_position,
                        gui_rects=[self.info_gui_rect])

                    if event.button == 3 and not is_mouse_on_gui:
                        Star(
                            x=mouse_x,
                            y=mouse_y,
                            mass=20000,
                            color=YELLOW
                        )

                if event.type == pygame.MOUSEBUTTONUP and not is_mouse_on_gui:
                    if event.button == 1:
                        try:
                            # Creating planet
                            Planet(
                                x=mouse_x,
                                y=mouse_y,
                                velocity_x=velocity_vector.x,
                                velocity_y=velocity_vector.y,
                                mass=150,
                                color=FOREST_GREEN
                            )

                            # Setting labels
                            self.info_gui_elements['velocity_x_label'].set_text('X velocity: None')
                            self.info_gui_elements['velocity_y_label'].set_text('Y velocity: None')

                        except Exception as error:
                            print('Velocity vector is not defined')

            pressed = pygame.mouse.get_pressed()  # Pressed buttons
            if pressed[0] and not is_mouse_on_gui:
                # Mouse position (x, y)
                current_mouse_position = pygame.mouse.get_pos()
                current_mouse_x, current_mouse_y = current_mouse_position

                # Calculating velocity vector
                current_pos_vector = Vector2(current_mouse_x, current_mouse_y)
                pressed_pos_vector = Vector2(mouse_x, mouse_y)
                velocity_vector = -(current_pos_vector - pressed_pos_vector) * pv_velocity_value_coef

                # Setting labels
                self.info_gui_elements['velocity_x_label'].set_text(f'X velocity: {round(velocity_vector.x, 4)}')
                self.info_gui_elements['velocity_y_label'].set_text(f'Y velocity: {-round(velocity_vector.y, 4)}')

                # Drawing preview
                pygame.draw.circle(self.screen, WHITE, (mouse_x, mouse_y), pv_radius)
                pygame.draw.line(self.screen, WHITE,
                                 (mouse_x, mouse_y),
                                 (mouse_x + velocity_vector.x * pv_line_length_coef,
                                  mouse_y + velocity_vector.y * pv_line_length_coef), pv_line_thickness)

                self.gui_manager.manager.process_events(event)

            # --- Updating elements of game  --- #

            # Simulation objects
            celestial_bodies.update()
            self.screen.blit(simulation_surface, (0, 0))
            celestial_bodies.draw(self.screen)

            # GUI
            pygame.draw.rect(self.screen, self.gui_manager.gui_rect_color, self.info_gui_rect)
            self.info_gui_elements['FPS_counter'].set_text(f'FPS: {int(self.clock.get_fps())}') # FPS
            self.gui_manager.manager.update(self.time_delta)
            self.gui_manager.manager.draw_ui(self.screen)

            # Display
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
