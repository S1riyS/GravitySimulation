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

        self.init_gui()

    def init_gui(self):
        # Statements of window
        self.is_dialogue_open = False
        self.is_planet_window_open = False
        self.is_star_window_open = False

        # ----- GUI ----- #
        self.gui_manager = GUIManager()

        # Rects
        self.info_gui_rect = self.gui_manager.get_gui_rect(self.gui_manager.info_block, 5)
        self.settings_gui_rect = self.gui_manager.get_gui_rect(self.gui_manager.settings_block, 5)

        # --- Info block --- #
        self.info_gui_elements = self.gui_manager.info_block['elements']

        fps_counter = self.info_gui_elements['FPS_counter']
        fps_counter.bg_colour = pygame.Color('#1b2933')
        fps_counter.font = pygame.font.Font(None, 26)

        # --- Settings block --- #
        # Elements
        self.settings_gui_elements = self.gui_manager.settings_block['elements']
        self.settings_gui_windows = self.gui_manager.settings_block['windows']

        title = self.settings_gui_elements['title']
        title.bg_colour = pygame.Color('#1b2933')
        title.font = pygame.font.Font(None, 34)
        title.rebuild()

        planet_title = self.settings_gui_elements['planet_title']
        planet_title.bg_colour = pygame.Color(0, 0, 0, 0)
        planet_title.font = pygame.font.Font(None, 28)
        planet_title.rebuild()

        mass_label = self.settings_gui_elements['mass_label']
        mass_label.bg_colour = pygame.Color(0, 0, 0, 0)
        mass_label.rebuild()

        # Windows
        self.planet_color_picker = self.settings_gui_windows['planet_color_picker']
        self.planet_color_picker.hide()
        print(self.planet_color_picker.is_focused)

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
        self.is_running = True
        while self.is_running:
            # Checking if any of windows are open
            self.is_dialogue_open = self.is_planet_window_open or self.is_star_window_open
            print(self.is_planet_window_open)

            # Filling surfaces
            simulation_surface.fill((0, 0, 0, 0))
            self.screen.fill(DARK_BLUE)

            self.clock.tick(FPS)
            self.time_delta = self.clock.tick(FPS) / 1000.0

            # Event loop
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    self.is_running = False

                # User events
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.settings_gui_elements['planet_color_button']:
                            if not self.is_planet_window_open:
                                self.planet_color_picker.show()

                            self.is_planet_window_open = True

                    if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                        if event.ui_element == self.planet_color_picker:
                            self.is_planet_window_open = False

                # Mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse position
                    pressed_mouse_position = pygame.mouse.get_pos()
                    mouse_x, mouse_y = pressed_mouse_position

                    # Checking if mouse on GUI
                    is_mouse_on_gui = self.mouse_collision_with_gui(
                        mouse_position=pressed_mouse_position,
                        gui_rects=[self.info_gui_rect, self.settings_gui_rect]) or self.is_dialogue_open

                    if event.button == 3 and not is_mouse_on_gui:
                        # Creating a star
                        Star(
                            x=mouse_x,
                            y=mouse_y,
                            mass=20000,
                            color=YELLOW
                        )

                if event.type == pygame.MOUSEBUTTONUP and not is_mouse_on_gui:
                    if event.button == 1:
                        try:
                            # Creating a planet
                            Planet(
                                x=mouse_x,
                                y=mouse_y,
                                velocity_x=velocity_vector.x,
                                velocity_y=velocity_vector.y,
                                mass=self.settings_gui_elements['mass_slider'].get_current_value(),
                                color=FOREST_GREEN
                            )

                            # Setting labels
                            self.info_gui_elements['velocity_x_label'].set_text('X velocity: None')
                            self.info_gui_elements['velocity_y_label'].set_text('Y velocity: None')

                        except Exception as error:
                            print(f'Velocity vector is not defined. Error: {error}')

                self.gui_manager.manager.process_events(event)

            # Drawing line of velocity of new planet
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

            # --- Updating elements of game --- #

            # Simulation objects
            celestial_bodies.update()
            self.screen.blit(simulation_surface, (0, 0))
            celestial_bodies.draw(self.screen)

            # GUI
            pygame.draw.rect(self.screen, self.gui_manager.gui_rect_color, self.info_gui_rect)
            pygame.draw.rect(self.screen, self.gui_manager.gui_rect_color, self.settings_gui_rect)
            self.info_gui_elements['FPS_counter'].set_text(f'FPS: {int(self.clock.get_fps())}')  # FPS
            self.gui_manager.manager.update(self.time_delta)
            self.gui_manager.manager.draw_ui(self.screen)

            # Display
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
