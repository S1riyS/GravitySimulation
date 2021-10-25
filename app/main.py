"""
Main project file, that containing game loop
"""

# Modules
import copy
from typing import Optional

import pygame
from pygame.math import Vector2
import pygame_gui
from pygame_gui.windows import UIColourPickerDialog

from app.config import *
from app.gui import GUIManager  # Importing entire GUI

pygame.init()


class Game:
    def __init__(self):
        # PyGame screen variables
        self.screen = pygame.display.set_mode(WINDOW_SIZE)  # Initialize screen
        pygame.display.set_caption("Gravity Simulation")  # Caption
        self.clock = pygame.time.Clock()  # Clock

        # Initiating beginning colors
        self.current_planet_color = copy.copy(FOREST_GREEN)
        self.current_star_color = copy.copy(YELLOW)

        # Grid surface
        self.is_drawing_grid = True
        self.grid_surface = pygame.Surface(WINDOW_SIZE).convert_alpha()
        self.grid_surface.fill((0, 0, 0, 0))

        self.init_gui()  # Initiating GUI

    @staticmethod
    def set_style(element: pygame_gui.elements, bg_color: Optional[pygame.Color] = None,
                  font_size: Optional[int] = None) -> None:
        """
        Static method that applying style to element of GUI
        :param element: element of GUI
        :param bg_color: Background color of element
        :param font_size: Font size
        :return: None
        """

        if bg_color is not None:
            element.bg_colour = pygame.Color(bg_color)
        if font_size is not None:
            element.font = pygame.font.Font(None, font_size)

        element.rebuild()

    @staticmethod
    def mouse_collision_with_gui(mouse_position: tuple, gui_rects: list) -> bool:
        """
        Return True if mouse on any of GUI rects and False if it isn't
        :param gui_rects: Rect of group of GUI elements
        :param mouse_position: Mouse position (x, y)
        :return: bool
        """

        return any([rect.collidepoint(mouse_position) for rect in gui_rects])

    @staticmethod
    def set_button_color(button: pygame_gui.elements.UIButton, color: pygame.Color):
        button.colours['normal_bg'] = color
        button.rebuild()

    def draw_grid(self, surface: pygame.Surface, color: pygame.Color, distance: int):
        if self.is_drawing_grid:
            for x in range(int(WIDTH / distance) + 2):
                pygame.draw.line(surface, color, (x * distance, 0), (x * distance, HEIGHT), 1)
            for y in range(int(HEIGHT / distance) + 2):
                pygame.draw.line(surface, color, (0, y * distance), (WIDTH, y * distance), 1)

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
        self.set_style(self.info_gui_elements['FPS_counter'], pygame.Color('#1b2933'), 26)

        # --- Settings block --- #
        # Elements
        self.settings_gui_elements = self.gui_manager.settings_block['elements']

        self.set_style(self.settings_gui_elements['title'], pygame.Color('#1b2933'), 34)

        # -- Planet -- #
        self.set_style(self.settings_gui_elements['planet_title'], pygame.Color(0, 0, 0, 0), 28)
        self.set_style(self.settings_gui_elements['planet_mass_label'], pygame.Color(0, 0, 0, 0))
        self.set_style(self.settings_gui_elements['planet_color_surface'], self.current_planet_color)

        # Planet windows
        self.planet_color_button = self.settings_gui_elements['planet_color_button']
        self.planet_color_picker = None

        # -- Star -- #
        self.set_style(self.settings_gui_elements['star_title'], pygame.Color(0, 0, 0, 0), 28)
        self.set_style(self.settings_gui_elements['star_mass_label'], pygame.Color(0, 0, 0, 0))
        self.set_style(self.settings_gui_elements['star_color_surface'], self.current_star_color)

        # Star windows
        self.star_color_button = self.settings_gui_elements['star_color_button']
        self.star_color_picker = None

        # -- General -- #
        self.set_style(self.settings_gui_elements['general_title'], pygame.Color(0, 0, 0, 0), 28)
        self.set_style(self.settings_gui_elements['grid_label'], pygame.Color(0, 0, 0, 0))

        self.set_button_color(self.settings_gui_elements['grid_button'], pygame.Color(121, 190, 112))

    def run(self):
        # Import everything necessary from objects
        from app.objects import simulation_surface, celestial_bodies, Planet, Star

        # Game loop
        self.is_running = True
        while self.is_running:
            # Checking if any of windows are open
            self.is_dialogue_open = self.is_planet_window_open or self.is_star_window_open

            # Filling surfaces
            simulation_surface.fill((0, 0, 0, 0))
            self.grid_surface.fill((0, 0, 0, 0))
            self.screen.fill(DARK_BLUE)

            # Drawing grid
            self.draw_grid(self.grid_surface, grid_color, grid_distance)

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
                        # If pressed planet's "choose color" button
                        if event.ui_element == self.planet_color_button:
                            self.is_planet_window_open = True
                            self.planet_color_picker = UIColourPickerDialog(pygame.Rect(210, 0, 390, 390),
                                                                            window_title='Planet color ...',
                                                                            initial_colour=self.current_planet_color,
                                                                            manager=self.gui_manager.manager)
                            self.planet_color_button.disable()

                        # If pressed star's "choose color" button
                        if event.ui_element == self.star_color_button:
                            self.is_star_window_open = True
                            self.star_color_picker = UIColourPickerDialog(pygame.Rect(230, 30, 390, 390),
                                                                          window_title='Star color ...',
                                                                          initial_colour=self.current_star_color,
                                                                          manager=self.gui_manager.manager)
                            self.star_color_button.disable()

                        if event.ui_element == self.settings_gui_elements['grid_button']:
                            if self.is_drawing_grid:
                                self.set_button_color(self.settings_gui_elements['grid_button'],
                                                      pygame.Color(231, 60, 62))
                            else:
                                self.set_button_color(self.settings_gui_elements['grid_button'],
                                                      pygame.Color(121, 190, 112))

                            self.is_drawing_grid = not self.is_drawing_grid

                    if event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                        # If picked color of planet
                        if event.ui_element == self.planet_color_picker:
                            self.current_planet_color = event.colour
                            self.set_style(self.settings_gui_elements['planet_color_surface'],
                                           self.current_planet_color)

                        # If picked color of star
                        if event.ui_element == self.star_color_picker:
                            self.current_star_color = event.colour
                            self.set_style(self.settings_gui_elements['star_color_surface'],
                                           self.current_star_color)

                    if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                        # If closed planet's "Colour Picker Dialog"
                        if event.ui_element == self.planet_color_picker:
                            self.is_planet_window_open = False
                            self.planet_color_button.enable()
                            self.planet_color_picker = None

                        # If closed star's "Colour Picker Dialog"
                        if event.ui_element == self.star_color_picker:
                            self.is_star_window_open = False
                            self.star_color_button.enable()
                            self.star_color_picker = None

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
                            mass=self.settings_gui_elements['star_mass_slider'].get_current_value(),
                            color=self.current_star_color
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
                                mass=self.settings_gui_elements['planet_mass_slider'].get_current_value(),
                                color=self.current_planet_color
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

            self.screen.blit(self.grid_surface, (0, 0))
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
